import os
import paho.mqtt.client as mqtt


def on_connect(client, _, __, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(os.getenv('MQTT_TOPIC'))


def on_message(_, __, msg):
    print(msg.topic + " " + str(msg.payload))


def run_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(os.getenv('MQTT_BROKER_USER'), os.getenv('MQTT_BROKER_PASSWORD'))

    client.connect(os.getenv('MQTT_BROKER_HOST'))

    client.loop_forever()


if __name__ == '__main__':
    run_mqtt()
