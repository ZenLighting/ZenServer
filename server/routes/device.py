from server.device.tracker import DeviceTracker
from flask import Blueprint, Flask, request
import colorsys
#from server.controllers.device_controller import DeviceController 
from server.device.registry import DeviceRegistry
from server.types.messages.device_registration import DeviceRegistrationMessage
#from server.model.light import DeviceEncoder
#from server.hub.server import LightServer
#from server.model.light import LightDevice

from server.model.sql_model import LightDevice
from server.device.light_device_manager import LightManager
from server.model.database import DatabaseSession
import json
import time

def attach_blueprint(app: Flask):
    container = app.container
    device_tracker: DeviceTracker = container.tracker
    state_manager: LightManager = container.light_state_manager
    #registry: DeviceRegistry = container.device_registry
    device_bp = Blueprint("device", __name__)

    @device_bp.route("/")
    def list_devices():
        with DatabaseSession() as session:
            light_objects = session.query(LightDevice).all()
        return {
            "status": 200,
            "data": {
                light_objects
            }
        }
    
    @device_bp.route("/active")
    def list_active_devices():
        return {
            "status": 200,
            "data":{
                "active_devices": device_tracker.devices_recieved
            }
        }
        #return json.dumps(registry.list_registered_macs())

    @device_bp.route("/register/<dId>")
    def register_active_device(dId):
        body = request.json
        light_mapping = body.get('light_mapping')
        description = body.get("description")

        if light_mapping is None:
            return {
                "status": 500,
                "message": f"a light mapping is required when registering light"
            }
        active_device = device_tracker.devices_recieved.get(dId)
        if active_device is None:
            return {
                "status": 404,
                "message": f"no active device found with id {dId}"
            }

        with DatabaseSession() as session:
            # check if dId already registered
            existing_device = session.query(LightDevice)\
                .filter(LightDevice.device_id==dId).one()
            if existing_device is not None:
                return {
                    "status": 400,
                    "message": f"light device {dId} is already registered"
                }
            
            active_device = DeviceRegistrationMessage(**active_device)
            new_device = LightDevice()
            new_device.device_id = active_device.dId
            new_device.light_amount = len(active_device.data['state'])
            new_device.light_mapping = light_mapping
            new_device.description = description
            session.add(new_device)
            session.commit()
            state_manager.update_from_db()
        return {
            "status": 200,
            "data": {
                "new_object": new_device.__dict__
            }
        }
    
    @device_bp.route("/<device_id>/assign_room", methods=["POST"])
    def assign_light_room(device_id):
        body = request.json
        room_id = body.get('room')
        room_x = body.get('position')['x']
        room_y = body.get('position')['y']

        with DatabaseSession() as session:
            lightObject = session.query(LightDevice).filter(LightDevice.device_id==device_id).one()
            lightObject.room = room_id
            lightObject.room_x = room_x
            lightObject.room_y = room_y
            session.commit()

        state_manager.update_from_db()

        return {
            "status": 200,
            "data": lightObject
        }
    
    @device_bp.route("/<device_id>/set_static")
    def assign_light_color(device_id: str):
        body = request.json
        color_style = body['color_scheme']
        color_value = body['value']
        # convert to rgb
        if color_style == "hsv":
            (r, g, b) = colorsys.hsv_to_rgb(*color_value)
        elif color_style == "hex":
            color_value = color_value.strip("#")
            r = int(color_value[:2], 16)
            g = int(color_value[2:4], 16)
            b = int(color_value[4:6], 16)
        elif color_style == "rgb":
            [r, g, b] = color_value
        #TODO: put rgb on light
        state_manager.light_objects.get(device_id).set_all(r, g, b)
        return {
            "status": 200,
            "data": "OK"
        }
    @device_bp.route("/<device_id>/set_animation")
    def assign_light_animation(device_id):
        return {
            "status": 404,
            "data": "Route is not yet set up but is planned for future"
        }

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