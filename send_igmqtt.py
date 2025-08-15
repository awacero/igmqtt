#!/usr/bin/env seiscomp-python

import sys, os, json, ast
sys.path.append( os.path.join(os.environ['SEISCOMP_ROOT'],'share/gds/tools/'))
import logging
import logging.config

import paho.mqtt.client as mqtt
from lib import bulletin, spooler

# Logging setup
logging_file = os.path.join(os.environ['SEISCOMP_ROOT'], 'var/log/', 'gds_service_igmqtt.log')
logging.basicConfig(filename=logging_file, format='%(asctime)s %(message)s')
logger = logging.getLogger("igmqtt")
logger.setLevel(logging.DEBUG)


class igmqttConfig:
    def __init__(self, config):
        prefix = 'mqtt'
        try:
            self.mqtt_file = config.get(prefix, "mqtt_auth_file")
        except:
            logger.info("##There is no igmqtt_db_credential defined")
            self.mqtt_file = None


class SpoolSendIGMQTT(spooler.Spooler):
    def __init__(self):
        spooler.Spooler.__init__(self)
        self._conf = igmqttConfig(self._config)
        logger.info("##Configuration File Loaded")

    def _read_server_file(self, json_file):
        try:
            with open(json_file) as json_data_files:
                return json.load(json_data_files)
        except Exception as e:
            raise Exception(f"##Error while reading JSON file: {e}")

    def _publish_to_mqtt(self, mqtt_info, message):
        try:
            logger.info("Start to publish")
            #client = mqtt.Client(mqtt_info["client_id"])
            client = mqtt.Client(client_id=mqtt_info["client_id"], protocol=mqtt.MQTTv311)
            client.username_pw_set(mqtt_info["username"], mqtt_info["pass"])
            client.connect(mqtt_info["broker"], int(mqtt_info["port"]))
            client.loop_start()
            #client.publish(mqtt_info["topic"], json.dumps(message))
            logger.info("CTM2")
            client.publish(mqtt_info["topic"],message)
            client.loop_stop()
            client.disconnect()
            logger.info("##MQTT message published successfully")
        except Exception as e:
            raise Exception(f"##Error publishing to MQTT: {e}")

    def spool(self, addresses, content):
        logger.info("##Starting spool() for send_igmqtt via MQTT")

        try:
            event_bulletin = bulletin.Bulletin()
            event_bulletin.read(content)
            event_data = event_bulletin.plain
            
        except Exception as e:
            raise Exception(f"##Error parsing event bulletin: {e}")
        
        for address in addresses:
            try:
                
                
                mqtt_creds = self._read_server_file(self._conf.mqtt_file)
                mqtt_info = mqtt_creds[address[1]]  # e.g., "TESTMQTT"
                self._publish_to_mqtt(mqtt_info, event_data)
            except Exception as e:
                self.addTargetError(address[0], address[1], e)
                logger.info("##Error in MQTT send: %s" % e)
                raise


if __name__ == "__main__":
    app = SpoolSendIGMQTT()
    app()

