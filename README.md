# virtual-sunrise
Tiny pyhton service to simulate a sunrise in my bedroom. Depends on zigbee2mqtt and an mqtt broker.

## Configuration
The following environment variables have to be set:
- `MQTT_BROKER_HOST` Ip or host name of the mqtt broker (the default port is going to be used)
- `MQTT_BROKER_USER` Username to authenticate with the mqtt broker
- `MQTT_BROKER_PASSWORD` Password to authenticate with the mqtt broker
- `MQTT_TOPIC` Topic to listen to (any message to this topic will trigger the sunrise)