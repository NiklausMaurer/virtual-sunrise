import json
import logging
import math
import os
import sys
import time

import paho.mqtt.client as mqtt

from sunrise.curves.path import Path, Point
from sunrise.curves.step import Step
from sunrise.stoppable_thread import StoppableThread
from sunrise.stopwatch import Stopwatch


class Sunrise:

    def __init__(self):
        self.thread = None

    def run(self):
        self.initialize_logging()
        self.start_mqtt_client()

    def on_message(self, client, __, message):
        logging.info("Message received.")
        if message.topic == os.getenv('MQTT_TOPIC_ABORT'):
            if self.thread is not None and self.thread.is_alive():
                logging.info("Aborting sunrise.")
                self.thread.stop()
            else:
                logging.info("No sunrise to abort.")
            return

        if message.topic == os.getenv('MQTT_TOPIC_START'):
            if self.thread is not None and self.thread.is_alive():
                logging.info("Sunrise already running.")
                return
            logging.info("Starting sunrise.")
            self.thread = StoppableThread(None, self.rise_color, None, (client, 'Office Left', 'Office Right'))
            self.thread.start()

    @staticmethod
    def on_connect(client, __, ___, rc, ____):
        logging.info(f"Connected to mqtt broker. Return code: {rc}")

        topic = os.getenv('MQTT_TOPIC_START')
        logging.info(f"Subscribing to topic {topic}")
        client.subscribe(topic)

        topic = os.getenv('MQTT_TOPIC_ABORT')
        logging.info(f"Subscribing to topic {topic}")
        client.subscribe(topic)

    @staticmethod
    def project_integer(curve, duration_seconds, t_seconds):
        if t_seconds > duration_seconds:
            return None
        return math.floor(curve(t_seconds / duration_seconds))

    @staticmethod
    def project(curve, duration_seconds, t_seconds):
        if t_seconds > duration_seconds:
            return None
        return curve(t_seconds / duration_seconds)

    def rise_color(self, client, *names):
        # idea: 3 phases: red -> orange, brightness, orange to white
        overall_duration = 50  # seconds
        topics = [f"zigbee2mqtt/{name}/set" for name in names]
        color_path = Path(Point(0.735, 0.265),
                          Point(0.642, 0.354),
                          Point(0.599, 0.391),
                          Point(0.554, 0.426),
                          Point(0.502, 0.434),
                          Point(0.443, 0.410))
        stopwatch = Stopwatch()
        current_time = stopwatch.time()
        while current_time < overall_duration:

            if self.thread.stopped():
                self.publish(client, topics, {"state": "OFF"})
                break

            color = self.project(color_path, overall_duration, current_time)
            payload = {
                "brightness": self.project_integer(Step(1, 250, 0.4, 0.9), overall_duration, current_time),
                "color": {
                    "x": color.x,
                    "y": color.y
                },
            }

            self.publish(client, topics, payload)

            time.sleep(0.3)
            current_time = stopwatch.time()

    @staticmethod
    def publish(client, topics, payload):
        payload_serialized = json.dumps(payload)
        logging.debug(f"Publishing to topics {','.join(topics)}. Payload: {payload_serialized}")
        for topic in topics:
            client.publish(topic, payload_serialized)

    def start_mqtt_client(self):
        client = mqtt.Client(protocol=mqtt.MQTTv5)
        client.on_message = self.on_message
        client.on_connect = self.on_connect

        client.on_subscribe = lambda _, __, ___, reason_codes, _____: logging.info(
            f"Subscribed successfully. Reason codes: {', '.join([c.getName() for c in reason_codes])}")
        client.on_connect_fail = lambda _, __: logging.info("Unable to connect to mqtt broker")
        client.username_pw_set(os.getenv('MQTT_BROKER_USER'), os.getenv('MQTT_BROKER_PASSWORD'))

        host = os.getenv('MQTT_BROKER_HOST')

        logging.info(f"Connecting to {host}")
        client.connect(host)

        client.loop_forever()

    @staticmethod
    def initialize_logging():
        root = logging.getLogger()
        root.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        root.addHandler(handler)
