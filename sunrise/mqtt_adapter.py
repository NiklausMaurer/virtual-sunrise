import json
import logging

import paho.mqtt.client as mqtt

from sunrise.settings import Settings


class MqttAdapter:

    def __init__(self,
                 settings: Settings,
                 mqtt_client: mqtt.Client,
                 on_start,
                 on_abort
                 ):
        self.on_start = on_start
        self.on_abort = on_abort
        self.settings = settings
        self.client = mqtt_client
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect

        self.client.on_subscribe = lambda _, __, ___, reason_codes, _____: logging.info(
            f"Subscribed successfully. Reason codes: {', '.join([c.getName() for c in reason_codes])}")
        self.client.on_connect_fail = lambda _, __: logging.info("Unable to connect to mqtt broker")
        self.client.username_pw_set(self.settings.mqtt_broker_user, self.settings.mqtt_broker_password)

        host = self.settings.mqtt_broker_host
        logging.info(f"Connecting to {host}")
        self.client.connect(host)

    def run(self):
        self.client.loop_forever()

    def on_connect(self, client, __, ___, rc, ____):
        logging.info(f"Connected to mqtt broker. Return code: {rc}")

        topic = self.settings.topic_start
        logging.info(f"Subscribing to topic {topic}")
        client.subscribe(topic)

        topic = self.settings.topic_abort
        logging.info(f"Subscribing to topic {topic}")
        client.subscribe(topic)

    def on_message(self, _, __, message):
        logging.info("Message received.")
        if message.topic == self.settings.topic_abort:
            self.on_abort()
        if message.topic == self.settings.topic_start:
            self.on_start()

    def publish(self, topics, payload):
        payload_serialized = json.dumps(payload)
        for topic in topics:
            logging.debug(f"Publishing to topic {topic}. Payload: {payload_serialized}")
            self.client.publish(topic, payload_serialized)
