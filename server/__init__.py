import logging
from flask import Flask, render_template, send_from_directory, send_file
#import server.routes.device as device_route
#import server.routes.rooms as room_route
#rom server.rooms.roomRegistry import RoomRegistry
from flask_cors import CORS
from server.mqtt.mqtt_service import MqttService
import paho.mqtt.client as mqtt
from server.queues.queue_manager import InputQueueManager
from server.device.tracker import DeviceTracker
from server.device.light_device_manager import LightManager
import server.routes.device as device_route
import settings


class Container(object):
    def __init__(self):
        self.input_queue_manager = InputQueueManager()
        self.mqtt_client = mqtt.Client()
        self.mqtt_service = MqttService(self.mqtt_client, self.input_queue_manager, settings.MQTT_HOST)
        self.tracker = DeviceTracker(self.input_queue_manager)
        self.light_state_manager = LightManager(self.mqtt_service)
        #self.mqtt_client = MqttService()
        #self.device_registry = DeviceRegistry()
        #self.room_registry = RoomRegistry()

        #self.udp_finder = UDPFinder(self.device_registry)
        #self.inifinity_thread = Thread(target=self.find_infinite_thread)

    def find_infinite_thread(self):
        while True:
            self.udp_finder.run_find_thread()

    def start(self):
        #self.mqtt_client.loop_start()
        self.tracker.start()

class App(object):
    def __init__(self, mqtt_host="localhost"):
        logging.basicConfig(level=logging.DEBUG)
        
        app = Flask(__name__, static_folder="./static", static_url_path="/static")
        CORS(app)
        container = Container()
        app.container = container
        

        
        #device_route.attach_blueprint(app)
        #room_route.attach_blueprint(app)
        device_route.attach_blueprint(app)
        """@app.route("/")
        def root():
            return render_template('index.html')
        
        @app.route("/<path:path>")
        def root_path(path):
            return render_template('index.html')"""

        container.start()
        app.run(host='0.0.0.0')
