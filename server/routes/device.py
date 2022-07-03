from flask import Blueprint, Flask, request
#from server.controllers.device_controller import DeviceController 
from server.device.registry import DeviceRegistry
#from server.model.light import DeviceEncoder
#from server.hub.server import LightServer
#from server.model.light import LightDevice
from server.model.sqlite_models import LightDeviceORM, LightDeviceModel
from server.model.light import LightDeviceWrapper
import json
import time
from sqlalchemy.orm import Session
import colorsys


def create_blueprint(registry: DeviceRegistry, session_maker: Session):
    device_bp = Blueprint("device", __name__)

    @device_bp.route("/")
    def list_light_devices():
        as_json = list(map(lambda x: x.model_object.json(), registry.devices))
        return {
            "devices": as_json
        }

    @device_bp.route("/<id>", methods=['GET'])
    def get_detailed_info(id: str):
        device: LightDeviceWrapper = registry.get_light_device(int(id))
        return {
            "grid": str(device.grid_object),
            "address": device.model_object.last_address,
            "object": device.model_object.json()
        }

    @device_bp.route("/<id>/set_color", methods=["POST"])
    def set_device_color(id):
        #light_controller.list_devices()
        #time.sleep(.5)
        body = request.json
        id = int(id)
        light_device= registry.get_light_device(id)
        color_protocol = body['color-protocol']
        if color_protocol == "hsv":
            h = float(body['h'])
            s = float(body['s'])
            v = float(body['v'])
            r, g, b = colorsys.hsv_to_rgb(h, s, v)
        else:
            r = int(body['r'])
            g = int(body['g'])
            b = int(body['b'])
        light_device.grid_object.set_grid_color(int(r), int(g), int(b))
        return {
            "status": "OK"
        }

    @device_bp.route("/", methods=["POST"])
    def create_device():
        body = request.json
        model = LightDeviceModel.parse_obj(body)
        # check if model already exists
        if registry.get_light_device(None, name=model.name) is not None:
            # update
            pass
        registry.add_light_device(model)
        return model.json()

    return device_bp