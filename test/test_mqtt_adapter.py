import unittest
from unittest.mock import Mock

from sunrise.mqtt_adapter import MqttAdapter
from sunrise.settings import Settings


class TestMqttAdapter(unittest.TestCase):

    def setUp(self):
        self.settings = Settings(
            topic_start='topic-start',
            topic_abort='topic-abort',
            sunrise_duration_seconds=10,
            sunrise_lights=['light1', 'light2'],
            mqtt_broker_host='mqtt-broker-host',
            mqtt_broker_user='mqtt-broker-user',
            mqtt_broker_password='mqtt-broker-password'
        )
        self.mqtt_client = Mock()
        self.mqtt_adapter = MqttAdapter(self.settings,
                                        self.mqtt_client,
                                        on_start_callback=Mock(),
                                        on_abort_callback=Mock())

    def test_run(self):
        self.mqtt_adapter.run()

        self.mqtt_client.loop_forever.assert_called_once()

    def test_on_connect(self):
        self.mqtt_adapter.on_connect(self.mqtt_client, None, None, 0, None)

        self.assertEqual(2, self.mqtt_client.subscribe.call_count)
        self.mqtt_client.subscribe.assert_any_call(self.settings.topic_start)
        self.mqtt_client.subscribe.assert_any_call(self.settings.topic_abort)

    def test_on_message_start(self):
        self.mqtt_adapter.on_message(None, None, Mock(topic=self.settings.topic_start))

        self.mqtt_adapter.on_start_callback.assert_called_once()
        self.mqtt_adapter.on_abort_callback.assert_not_called()

    def test_on_message_abort(self):
        self.mqtt_adapter.on_message(None, None, Mock(topic=self.settings.topic_abort))

        self.mqtt_adapter.on_abort_callback.assert_called_once()
        self.mqtt_adapter.on_start_callback.assert_not_called()

    def test_publish(self):
        self.mqtt_adapter.publish(['topic1', 'topic2'], {'key': 'value'})

        self.mqtt_client.publish.assert_any_call('topic1', '{"key": "value"}')
        self.mqtt_client.publish.assert_any_call('topic2', '{"key": "value"}')


if __name__ == '__main__':
    unittest.main()
