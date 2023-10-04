import base64
import os
from dataclasses import dataclass


@dataclass
class Settings:
    topic_start: str
    topic_abort: str
    sunrise_duration_seconds: int
    sunrise_lights: list[str]
    mqtt_broker_host: str
    mqtt_broker_user: str
    mqtt_broker_password: str

    def __init__(self, topic_start: str, topic_abort: str, sunrise_duration_seconds: int, sunrise_lights: list[str],
                 mqtt_broker_host: str,
                 mqtt_broker_user: str, mqtt_broker_password: str):
        self.sunrise_lights = sunrise_lights
        self.topic_start = topic_start
        self.topic_abort = topic_abort
        self.sunrise_duration_seconds = int(sunrise_duration_seconds)
        self.mqtt_broker_host = mqtt_broker_host
        self.mqtt_broker_user = mqtt_broker_user
        self.mqtt_broker_password = mqtt_broker_password


def get_settings() -> Settings:
    return Settings(
        topic_start=os.getenv('MQTT_TOPIC_START'),
        topic_abort=os.getenv('MQTT_TOPIC_ABORT'),
        sunrise_duration_seconds=int(os.getenv('SUNRISE_DURATION_SECONDS')),
        sunrise_lights = base64.b64decode(os.getenv('SUNRISE_LIGHTS')).decode("ascii").split(','),
        mqtt_broker_host=os.getenv('MQTT_BROKER_HOST'),
        mqtt_broker_user=os.getenv('MQTT_BROKER_USER'),
        mqtt_broker_password=os.getenv('MQTT_BROKER_PASSWORD')
    )
