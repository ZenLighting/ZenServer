import paho.mqtt.client as mqttt
import logging
from queue import Queue
from server.queues.queue_manager import InputQueueManager
import json

log = logging.getLogger(__name__)

class MqttService(object):

    def __init__(self, mqttClient: mqttt.Client,  queue_manager: InputQueueManager, host="localhost"):
        self.client = mqttClient
        self.client.connect(host=host)
        self.client.loop_start()

        self.registration_queue = queue_manager.get_queue("registration")

        self.client.subscribe("device/registry")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message



    def on_connect(self, client, userdata, flags, rc):
        log.info(f"Connected to mqtt server with code {str(rc)}")
        
    def on_message(self, client, userdata, message):
        log.debug(f"{message.topic}, {message.payload}")
        if message.topic == "device/registry":
            registration_message = json.loads(message.payload)
            self.registration_queue.put(registration_message)
    
    def get_client(self):
        return self.client

