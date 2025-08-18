# igmqtt

Tools to transform SeisComP event information into XML bulletins and send them to MQTT brokers.

## Overview
The repository contains two scripts intended to be used within a SeisComP environment:

- **`filter_igmqtt.py`** – Parses SeisComP event parameters and produces an `event_message` XML bulletin containing magnitude, location, depth and time information.
- **`send_igmqtt.py`** – Reads bulletins from the spool and publishes them to one or more MQTT brokers using credentials defined in a configuration file.

## Requirements
- SeisComP (provides the `seiscomp3` libraries and execution environment).
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

The key (e.g. `TESTMQTT`) is referenced by the addresses passed to the spooler.

## Usage
These scripts are typically run by SeisComP's GDS services:

- `filter_igmqtt.py` is used as a filter when an event is generated.
- `send_igmqtt.py` is invoked by the spooler to publish the bulletin to the configured MQTT brokers.

Example standalone execution:
```bash
seiscomp-python filter_igmqtt.py <event_parameters_file>
seiscomp-python send_igmqtt.py
```

Both scripts log to `var/log/gds_service_igmqtt.log` under the SeisComP root directory.

## Logging
Logs are written to `var/log/gds_service_igmqtt.log` inside `SEISCOMP_ROOT` for debugging and auditing.

## Examples
Reference files `EXAMPLE.send_igmqtt.cfg` and `EXAMPLE.mqtt_auth.json` show how to configure the service.

## License
This repository does not currently specify a license.

