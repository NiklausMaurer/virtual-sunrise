import os
import sys
import time
import threading
import json
import logging

import paho.mqtt.client as mqtt


def on_message(client, _, __):
    logging.info("Message received.")
    if threading.active_count() > 1:
        logging.warning(f"Aborting, active thread count is {threading.active_count()}. The sun is already rising.")
        return
    logging.info("Starting sunrise.")
    threading.Thread(None, rise_color, None, (client, 'Bedroom Right', 0, 5)).start()
    threading.Thread(None, rise_color, None, (client, 'Bedroom Left', 4 * 60, 3)).start()
    threading.Thread(None, rise_color, None, (client, 'Bedroom Back', 5 * 60, 3)).start()


def on_connect(client, __, ___, rc, ____):
    logging.info(f"Connected to mqtt broker. Return code: {rc}")

    topic = os.getenv('MQTT_TOPIC')
    logging.info(f"Subscribing to topic {topic}")
    client.subscribe(topic)


def rise_color(client, name, initial_delay=0, delay=4):
    time.sleep(initial_delay)
    count = 0
    while count < 255:
        progress = count / 255.0
        payload = {
            "brightness": count,
            "color": {
                "h": int(32 * progress),
                "hue": int(32 * progress),
                "s": (100 - 18 * progress),
                "saturation": (100 - 18 * progress),
                "x": 0.701 - 0.2411 * progress,
                "y": 0.299 + 0.1116 * progress
            },
            "color_mode": "xy"
        }
        count += 1

        topic = f"zigbee2mqtt/{name}/set"
        payload_serialized = json.dumps(payload)

        logging.debug(f"Publishing to topic {topic}. Payload: {payload_serialized}")
        client.publish(topic, payload_serialized)
        time.sleep(delay)


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
