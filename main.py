import os
import time
import threading

import paho.mqtt.client as mqtt


def on_connect(client, _, __, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(os.getenv('MQTT_TOPIC'))


def on_message(_, __, msg):
    print(msg.topic + " " + str(msg.payload))
    thread = threading.Thread(None, rise, None, ('first', 1))
    thread.start()
    thread2 = threading.Thread(None, rise, None, ('second', 1))
    thread2.start()


def rise(entity):
    count = 0
    while count < 5:
        time.sleep(0.5)
        count += 1
        print("%s: %s" % (entity, time.ctime(time.time())))


def run_mqtt():
    client = mqtt.Client()
    client.on_message = on_message
    client.username_pw_set(os.getenv('MQTT_BROKER_USER'), os.getenv('MQTT_BROKER_PASSWORD'))

    client.connect(os.getenv('MQTT_BROKER_HOST'))
    client.subscribe(os.getenv('MQTT_TOPIC'))

    client.loop_forever()


if __name__ == '__main__':
    run_mqtt()
