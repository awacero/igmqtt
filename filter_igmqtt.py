#!/usr/bin/env seiscomp-python

import sys,os
sys.path.append( os.path.join(os.environ['SEISCOMP_ROOT'],'share/gds/tools/')) 
import seiscomp3.Core
import seiscomp3.DataModel
from lib import bulletin
from lib.filter import Filter

from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

from datetime import datetime, timedelta,timezone
from ig_gds_utilities import ig_utilities as utilities 
import logging
import logging.config

logging_file = os.path.join(os.environ['SEISCOMP_ROOT'],'var/log/','gds_service_igmqtt.log')
logging.basicConfig(filename=logging_file, format='%(asctime)s %(message)s')
logger = logging.getLogger("igmqtt")
logger.setLevel(logging.DEBUG)

def _iso_utc_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def _pretty_xml(elem):
    rough = tostring(elem, encoding="utf-8")
    return minidom.parseString(rough).toprettyxml(indent="  ")



class igMQTTFilter(Filter):
    
    def filter(self,ep):

        logger.info("Starting filter for igmqtt")
        b=bulletin.Bulletin() 
        e=self.parse_event_parameters(ep)     
        b.plain=str(e)
        return str(b)
        

    def parse_event_parameters(self,ep):

        logger.info("Start parse_event_parameters")

        try:

            event={}
            event["id"]= ""
            event["lat"]    = ""
            event["lon"]    = ""
            event["description"] = ""
            event["magVal"] = ""
            event["magType"]=""
            event["timeSec"]= ""
            event["timeNow"]= ""
            event["depth"]  = ""
            event["status"]   = ""
            event["revision"]    = ""
            event["local_time"] = ""
            event["type"] = ""
    

            if ep.eventCount()>1:
                return event

            event_object = ep.event(0)
            event["id"] = event_object.publicID()

            for j in range(0,event_object.eventDescriptionCount()):
                ed = event_object.eventDescription(j)
                if ed.type() == seiscomp3.DataModel.REGION_NAME:
                    event["description"] = ed.text()
                    break

            magnitude = seiscomp3.DataModel.Magnitude.Find(event_object.preferredMagnitudeID())
            if magnitude:
                event['magVal'] = "%0.1f" %magnitude.magnitude().value()
                event["magType"]= magnitude.type()
            origin = seiscomp3.DataModel.Origin.Find(event_object.preferredOriginID())
            if origin:
                event["timeSec"] = origin.time().value().toString("%Y/%m/%d %H:%M:%S")
                event["timeNow"] = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                local_time=datetime.strptime(event["timeSec"],"%Y/%m/%d %H:%M:%S") -timedelta(hours=5)
                event["local_time"]   = local_time.strftime("%Y/%m/%d %H:%M:%S")
                
                event["lat"]  = "%.1f" % origin.latitude().value() 
                event["lon"]  = "%.1f" % origin.longitude().value()
                event["station_magnitude"]= "%s" %origin.magnitudeCount()
                
                try: event["depth"] = "%.1f" % origin.depth().value()
                except seiscomp3.Core.ValueException: event["depth"]="-"
                try: event["status"]  = "%s" %seiscomp3.DataModel.EEvaluationModeNames.name(ep.origin(0).evaluationMode())
                except: event["status"]="NOT SET"
                try:
                    typeDescription=event_object.type()
                    event["type"] = "%s" %seiscomp3.DataModel.EEventTypeNames.name(typeDescription)
                except: event["type"]="NOT SET"
                
                event['revision']    = '1'


                root = Element("event_message", {
                    "alg_vers": "1.1.1-2025-08-14",
                    "category": "live",
                    "instance": "igmqtt",
                    "message_type": "new",
                    "orig_sys": "SeisComP",
                    "ref_id": "0",
                    "ref_src": "",
                    "timestamp": _iso_utc_now(),
                    "version": "0"
                })
            logger.info("CTM")        
            
            core = SubElement(root, "core_info", {"id": event["id"]})
            SubElement(core, "mag", {"units":"M"}).text = event["magVal"]
            SubElement(core, "mag_uncer", {"units":"M"}).text = "0.1"
            SubElement(core, "lat", {"units":"deg"}).text = event["lat"]
            SubElement(core, "lat_uncer", {"units":"deg"}).text = "0.1"
            SubElement(core, "lon", {"units":"deg"}).text = event["lon"]
            SubElement(core, "lon_uncer", {"units":"deg"}).text = "0.1"
            SubElement(core, "depth", {"units":"km"}).text = event["depth"]
            SubElement(core, "depth_uncer", {"units":"km"}).text = "1.0"
            SubElement(core, "orig_time", {"units":"UTC"}).text = event["timeSec"]
            SubElement(core, "orig_time_uncer", {"units":"sec"}).text = "0.1"
            SubElement(core, "likelihood").text = "0.9000"
            SubElement(core, "num_stations").text = event["station_magnitude"]

 
            return _pretty_xml(root)
        except Exception as e:
            logger.info(f"Error in filter_igmqtt was: {e}")
            return -1

if __name__ == "__main__":
    app = igMQTTFilter()
    sys.exit(app())
