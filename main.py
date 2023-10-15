import paho.mqtt.client as mqtt


from sunrise.logging import initialize_logging
from sunrise.settings import get_settings
from sunrise.sunrise import Sunrise

if __name__ == '__main__':
    initialize_logging()
    settings = get_settings()
    mqtt_client = mqtt.Client(protocol=mqtt.MQTTv5)
    sunrise = Sunrise(settings, mqtt_client)
    sunrise.run()
