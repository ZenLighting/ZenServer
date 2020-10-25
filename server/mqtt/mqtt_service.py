import paho.mqtt.client as mqttt
import logging

log = logging.getLogger(__name__)

class MqttService(object):

    def __init__(self, mqttClient: mqttt.Client, host="localhost"):
        self.client = mqttClient
        self.client.connect(host=host)
        self.client.loop_start()

        self.client.subscribe("zen/#")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message


    def on_connect(self, client, userdata, flags, rc):
        log.info(f"Connected to mqtt server with code {str(rc)}")
        
    def on_message(self, client, userdata, message):
        log.debug(f"{message.topic}, {message.payload}")

    def get_client(self):
        return self.client

