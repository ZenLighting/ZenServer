from flask import Blueprint, Flask, request
from server.controllers.device_controller import DeviceController 
from server.model.light import DeviceEncoder
from server.hub.server import LightServer
import json
import time

def attach_blueprint(app: Flask):
    container = app.container
    light_controller: DeviceController = container.light_controller
    light_server: LightServer = container.light_server
    device_bp = Blueprint("device", __name__)

    @device_bp.route("/")
    def list_light_devices():
        light_device_map = light_controller.list_devices()
        print(light_device_map)
        return json.dumps(light_device_map, cls=DeviceEncoder)

    @device_bp.route("/<uuid>/set_color", methods=["POST"])
    def set_device_color(uuid):
        print(int(uuid))
        uuid = int(uuid)
        #light_controller.list_devices()
        #time.sleep(.5)
        body = request.json
        light_interface = light_server.get_light_mqtt_interface(uuid)
        r = body['r']
        g = body['g']
        b = body['b']
        brightness = body['brightness']
        light_interface.send_color(r, g, b, brightness)
        return "OK"

    app.register_blueprint(device_bp, url_prefix="/devices")