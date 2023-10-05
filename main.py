from sunrise.logging import initialize_logging
from sunrise.mqtt import Client
from sunrise.settings import get_settings
from sunrise.sunrise import Sunrise

if __name__ == '__main__':
    initialize_logging()
    settings = get_settings()
    mqtt_client = Client(settings)
    sunrise = Sunrise(settings, mqtt_client)
    sunrise.run()
