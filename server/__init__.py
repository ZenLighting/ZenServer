from server.finders.udpfinder import UDPFinder
from server.device.registry import DeviceRegistry
from server.model.light import LightDevice
from server.device.udpcommunicator import UDPCommunicator
from server.device.statemanager import StateManager
from threading import Thread
import logging
from flask import Flask, render_template, send_from_directory, send_file
import server.routes.device as device_route
import server.routes.rooms as room_route
from server.rooms.roomRegistry import RoomRegistry
from flask_cors import CORS

class Container(object):
    def __init__(self):
        self.device_registry = DeviceRegistry()
        self.room_registry = RoomRegistry()

        self.udp_finder = UDPFinder(self.device_registry)
        self.inifinity_thread = Thread(target=self.find_infinite_thread)

    def find_infinite_thread(self):
        while True:
            self.udp_finder.run_find_thread()

    def start(self):
        self.inifinity_thread.start()

class App(object):
    def __init__(self, mqtt_host="localhost"):
        logging.basicConfig(level=logging.DEBUG)
        
        app = Flask(__name__, static_folder="./static", static_url_path="/static")
        CORS(app)
        container = Container()
        app.container = container
        

        
        device_route.attach_blueprint(app)
        room_route.attach_blueprint(app)

        @app.route("/")
        def root():
            return render_template('index.html')
        
        @app.route("/<path:path>")
        def root_path(path):
            return render_template('index.html')

        container.start()
        app.run(host='0.0.0.0')
