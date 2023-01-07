import os
import time
import threading
import json

import paho.mqtt.client as mqtt


def on_message(client, _, __):
    print("Message received.")
    if threading.active_count() > 1:
        print(f"Aborting, active thread count is {threading.active_count()}. The sun is already rising.")
        return
    print("Starting sunrise.")
    threading.Thread(None, rise_color, None, (client, 'Bedroom Right', 0, 5)).start()
    threading.Thread(None, rise_color, None, (client, 'Bedroom Left', 4 * 60, 3)).start()
    threading.Thread(None, rise_color, None, (client, 'Bedroom Back', 5 * 60, 3)).start()


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
        client.publish(f'zigbee2mqtt/{name}/set', json.dumps(payload))
        time.sleep(delay)


def start_mqtt_client():
    client = mqtt.Client()
    client.on_message = on_message
    client.username_pw_set(os.getenv('MQTT_BROKER_USER'), os.getenv('MQTT_BROKER_PASSWORD'))
    client.connect(os.getenv('MQTT_BROKER_HOST'))
    client.subscribe(os.getenv('MQTT_TOPIC'))

    client.loop_forever()


if __name__ == '__main__':
    start_mqtt_client()
