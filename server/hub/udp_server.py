import socket
import logging
from typing import Dict
from paho.mqtt.client import MQTTMessage, Client
from server.hub.registry import LightRegistry
from server.mqtt.mqtt_service import MqttService
from server.hub.hub import LightMQTTConnection
import json
from threading import Thread
import time

log = logging.getLogger(__name__)

class LightUDPServer(Thread):

    def __init__(self, registry: LightRegistry):
        Thread.__init__(self)
        self.light_registry = registry
        self.mqtt: Client = mqttClient.get_client()
        self.mqtt.message_callback_add("zen/registration_response", self.register_light)
        self.id_to_obj_map = {}

    def register_light(self, client, userdata, message: MQTTMessage):
        print("here")
        print(message.payload)
        # parse the message
        message_parsed = json.loads(message.payload)
        light_id = message_parsed['uuid']
        led_number = message_parsed['num']
        light_grid_string = message_parsed['grid']

        light_data = self.light_registry.register_light(light_id, led_number, light_grid_string)
        light_obj = LightMQTTConnection(self.mqtt, light_data)
        self.id_to_obj_map[light_id] = light_obj
        print(self.id_to_obj_map)

    def run(self):
        while True:
            self.gather_lights()
            time.sleep(5)


    def gather_lights(self):
        self.mqtt.publish("zen/registration_request")

    def get_light_mqtt_interface(self, light_id) -> LightMQTTConnection:
        print(self.id_to_obj_map, light_id)
        return self.id_to_obj_map.get(light_id, None)


        
        
        