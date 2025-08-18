# Technical Analysis

## System Overview
The igmqtt project converts SeisComP event parameters into XML bulletins and publishes them to MQTT brokers. It consists of two cooperating scripts:

- `filter_igmqtt.py` – parses a single event and formats it into an `event_message` XML document.
- `send_igmqtt.py` – reads bulletins from the spooler and publishes them to configured MQTT brokers.

## Component Details
### filter_igmqtt.py
- Uses a shared log file located under `SEISCOMP_ROOT/var/log/gds_service_igmqtt.log` for diagnostics【F:filter_igmqtt.py†L18-L21】
- The `filter` method wraps parsed event parameters into a bulletin message【F:filter_igmqtt.py†L34-L40】
- `parse_event_parameters` validates that only one event is provided, extracts magnitude and origin details, and builds the XML `event_message` payload【F:filter_igmqtt.py†L65-L132】

### send_igmqtt.py
- Shares the same logging destination as the filter component for consistent tracing【F:send_igmqtt.py†L11-L15】
- `igmqttConfig` loads the path to broker credentials from the configuration file【F:send_igmqtt.py†L18-L25】
- `_publish_to_mqtt` establishes a Paho client, connects to the broker, and publishes the bulletin content to the designated topic【F:send_igmqtt.py†L41-L54】
- `spool` parses bulletin data and iterates over target addresses to deliver messages, collecting errors for failed targets【F:send_igmqtt.py†L58-L79】

## Data Flow
1. `filter_igmqtt.py` receives event parameters and outputs a formatted XML bulletin.
2. `send_igmqtt.py` reads the bulletin, loads broker credentials, and publishes the message via MQTT.

## External Dependencies
- **SeisComP libraries** for seismic data models.
- **Paho MQTT** client for message transport.

## Logging & Error Handling
Both components log progress and issues to the same log file to aid operational debugging. Critical operations, such as XML generation or MQTT publishing, are wrapped in `try/except` blocks so that errors are reported and raised for higher-level handling.

