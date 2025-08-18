# igmqtt

SCP-GDS plugin/service to transform SeisComP event information into XML to send them to MQTT clients.

## Overview
The repository contains two scripts intended to be used within a SeisComP environment:

- **`filter_igmqtt.py`** – Parses SCP-GDS event parameters and produces an `event_message` XML  containing magnitude, location, depth and time information.
- **`send_igmqtt.py`** – Reads XML bulletins from the spool and publishes them to one or more MQTT clients using credentials defined in a JSON auth file.

## Requirements
- SeisComP (provides the `seiscomp3` libraries and execution environment).
- GDS for libraries
- gds_utils from 
- [Paho MQTT](https://www.eclipse.org/paho/) client library.
- Python 3.

## Configuration
`send_igmqtt.py` expects a configuration file and a separate JSON file with MQTT connection details.

1. Create a configuration file (e.g. `send_igmqtt.cfg`):
   ```ini
   [mqtt]
   mqtt_auth_file = $PLUGIN_PATH/igmqtt/mqtt_auth.json
   hour_limit = 8760
   log_file = $PLUGING_PATH/igmqtt/send_igmqtt.log
   ```
2. Create `mqtt_auth.json` with one or more broker definitions:
   ```json
   {
     "TESTMQTT": {
       "broker": "test.mosquitto.org",
       "port": "1883",
       "topic": "test/gfast",
       "client_id": "iggfast",
       "username": "",
       "pass": ""
     }
   }
   ```

The key (e.g. `TESTMQTT`) is referenced by the addresses passed to the spooler. It is defined on GDS configuration web.  

## Usage
These scripts are typically run by SeisComP's GDS services:

- `filter_igmqtt.py` is used as a filter when an event is detected by SCP.
- `send_igmqtt.py` is invoked by the spooler to publish the bulletin to the configured MQTT brokers.

Example standalone execution:

***There is no way to run the scripts outside a SCP-GDS environment*** 


## Logging
Logs are written to `$SEISCOMP_ROOT/var/log/gds_service_igmqtt.log` for debugging and auditing.
Logs of the service running inside GDS are in `$CONFIG_DIR/log/gds.log`

## Examples
Reference files `EXAMPLE.send_igmqtt.cfg` and `EXAMPLE.mqtt_auth.json` show how to configure the service.

## License
This repository does not currently specify a license.

