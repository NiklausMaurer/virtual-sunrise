import os
import time
import threading
import json

import paho.mqtt.client as mqtt


def on_connect(client, _, __, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(os.getenv('MQTT_TOPIC'))


def on_message(client, __, msg):
    print(msg.topic + " " + str(msg.payload))
    threading.Thread(None, rise, None, (client, 'Living Room Right')).start()
    threading.Thread(None, rise, None, (client, 'Living Room Left', 30)).start()


def rise(client, name, delay = 0):
    time.sleep(delay)
    count = 0
    while count < 255:
        payload = {
            "brightness": count,
            "color_temp": int(454 - (count / 255.0) * (454 - 370))
        }
        time.sleep(1)
        count += 2
        print(name, json.dumps(payload))
        client.publish(f'zigbee2mqtt/{name}/set', json.dumps(payload))


def run_mqtt():
    client = mqtt.Client()
    client.on_message = on_message
    client.username_pw_set(os.getenv('MQTT_BROKER_USER'), os.getenv('MQTT_BROKER_PASSWORD'))

    client.connect(os.getenv('MQTT_BROKER_HOST'))
    client.subscribe(os.getenv('MQTT_TOPIC'))

    client.loop_forever()


if __name__ == '__main__':
    run_mqtt()
