from server.device.tracker import DeviceTracker
from flask import Blueprint, Flask, request
#from server.controllers.device_controller import DeviceController 
from server.device.registry import DeviceRegistry
#from server.model.light import DeviceEncoder
#from server.hub.server import LightServer
from server.model.light import LightDevice

import json
import time

def attach_blueprint(app: Flask):
    container = app.container
    device_tracker: DeviceTracker = container.tracker
    #registry: DeviceRegistry = container.device_registry
    device_bp = Blueprint("device", __name__)

    @device_bp.route("/")
    def list_devices():

    @device_bp.route("/active")
    def list_active_devices():
        return {
            "status": 200,
            "active_devices": device_tracker.devices_recieved
        }
        #return json.dumps(registry.list_registered_macs())

    """@device_bp.route("/<mac>", methods=['GET'])
    def get_detailed_info(mac: str):
        device: LightDevice = registry.get_light_device(mac)
        return {
            "grid": device.state.grid,
            "address": device.communicator.address,
            "mac": mac
        }"""

    """@device_bp.route("/<mac>/set_color", methods=["POST"])
    def set_device_color(mac):
        #light_controller.list_devices()
        #time.sleep(.5)
        body = request.json
        light_device= registry.get_light_device(mac)
        r = body['r']
        g = body['g']
        b = body['b']
        brightness = body['brightness']
        light_device.state.set_all(r, g, b)
        return {
            "status": "OK"
        }"""

    app.register_blueprint(device_bp, url_prefix="/devices")