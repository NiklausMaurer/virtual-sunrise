import os
import sys
import time
import threading
import json
import logging

import paho.mqtt.client as mqtt

from sunrise.curves.linear import Linear
from sunrise.curves.step import Step
from sunrise.stopwatch import Stopwatch


def on_message(client, _, __):
    logging.info("Message received.")
    logging.info("Starting sunrise.")
    threading.Thread(None, rise_color, None, (client, 'Living Room Right')).start()


def on_connect(client, __, ___, rc, ____):
    logging.info(f"Connected to mqtt broker. Return code: {rc}")

    topic = os.getenv('MQTT_TOPIC')
    logging.info(f"Subscribing to topic {topic}")
    client.subscribe(topic)

    on_message(client, None, None)


def project(curve, duration_seconds, t_seconds):
    if t_seconds > duration_seconds:
        return None
    return curve(t_seconds / duration_seconds)


def rise_color(client, name):
    watch = Stopwatch()

    while True:
        brightness = project(Step(50, 200, .5, .9), duration_seconds=10, t_seconds=watch())
        if brightness is None:
            break

        payload = {
            "brightness": brightness,
        }

        topic = f"zigbee2mqtt/{name}/set"
        payload_serialized = json.dumps(payload)

        logging.debug(f"Publishing to topic {topic}. Payload: {payload_serialized}")
        client.publish(topic, payload_serialized)
        time.sleep(0.3)


def start_mqtt_client():
    client = mqtt.Client(protocol=mqtt.MQTTv5)
    client.on_message = on_message
    client.on_connect = on_connect

    client.on_subscribe = lambda _, __, ___, reason_codes, _____: logging.info(
        f"Subscribed successfully. Reason codes: {', '.join([c.getName() for c in reason_codes])}")
    client.on_connect_fail = lambda _, __: logging.info("Unable to connect to mqtt broker")
    client.username_pw_set(os.getenv('MQTT_BROKER_USER'), os.getenv('MQTT_BROKER_PASSWORD'))

    host = os.getenv('MQTT_BROKER_HOST')

    logging.info(f"Connecting to {host}")
    client.connect(host)

    client.loop_forever()


def initialize_logging():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)


if __name__ == '__main__':
    initialize_logging()
    start_mqtt_client()
