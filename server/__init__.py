from server.hub.registry import LightRegistry
from paho.mqtt.client import Client
from server.mqtt.mqtt_service import MqttService
from server.hub.server import LightServer
from flask import Flask
import logging
import time
import server.routes.device as device_route
from server.controllers.device_controller import DeviceController

class Container(object):
    def __init__(self, mqtt_host="localhost"):
        
        self.mqtt_provider = Client()
        self.mqtt_service = MqttService(self.mqtt_provider, mqtt_host)

        self.light_registry = LightRegistry()
        self.light_server = LightServer(self.mqtt_service, self.light_registry)

        # controllers
        self.light_controller = DeviceController(self.light_server, self.light_registry)
        
        self.light_server.start()

class App(object):
    def __init__(self, mqtt_host="localhost"):
        logging.basicConfig(level=logging.DEBUG)
        
        app = Flask(__name__)
        
        container = Container(mqtt_host)
        app.container = container
        device_route.attach_blueprint(app)

        app.run()
