import logging
import time

from sunrise.curves.path import Path, Point
from sunrise.curves.projection import project, project_integer
from sunrise.curves.step import Step
from sunrise.mqtt_adapter import MqttAdapter
from sunrise.settings import Settings
from sunrise.stoppable_thread import StoppableThread
from sunrise.stopwatch import Stopwatch


class Sunrise:

    def __init__(self, settings: Settings, mqtt_client: MqttAdapter):
        self.settings = settings
        self.mqtt_client = mqtt_client
        self.thread = None
        self.mqtt_client = mqtt_client
        self.mqtt_client.set_on_start_callback(self.on_start)
        self.mqtt_client.set_on_abort_callback(self.on_abort)

    def run(self):
        self.mqtt_client.run()

    def on_start(self):
        if self.thread is not None and self.thread.is_alive():
            logging.info("Sunrise already running.")
            return
        logging.info("Starting sunrise.")
        self.thread = StoppableThread(None, self.rise_color, None)
        self.thread.start()

    def on_abort(self):
        if self.thread is not None and self.thread.is_alive():
            logging.info("Aborting sunrise.")
            self.thread.stop()
        else:
            logging.info("No sunrise to abort.")
        return

    def rise_color(self):
        overall_duration = self.settings.sunrise_duration_seconds
        lights = self.settings.sunrise_lights
        topics = [f"zigbee2mqtt/{light}/set" for light in lights]
        color_path = Path(Point(0.735, 0.265),
                          Point(0.642, 0.354),
                          Point(0.599, 0.391),
                          Point(0.554, 0.426),
                          Point(0.502, 0.418),
                          Point(0.443, 0.410))
        stopwatch = Stopwatch()
        current_time = stopwatch.time()
        while current_time < overall_duration:

            if self.thread.stopped():
                self.mqtt_client.publish(topics, {"state": "OFF"})
                break

            color = project(color_path, overall_duration, current_time)
            payload = {
                "brightness": project_integer(Step(1, 250, 0.4, 0.9), overall_duration, current_time),
                "color": {
                    "x": color.x,
                    "y": color.y
                },
            }

            self.mqtt_client.publish(topics, payload)

            time.sleep(1)
            current_time = stopwatch.time()
