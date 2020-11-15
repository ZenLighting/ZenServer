from flask import Blueprint, Flask, request
#from server.controllers.device_controller import DeviceController 
from server.device.registry import DeviceRegistry
from server.rooms.room import Room
from server.rooms.roomRegistry import RoomRegistry
#from server.model.light import DeviceEncoder
#from server.hub.server import LightServer
import json
import time

class MyEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__    

def attach_blueprint(app: Flask):
    container = app.container
    light_registry: DeviceRegistry = container.device_registry
    registry: RoomRegistry = container.room_registry
    room_bp = Blueprint("room", __name__)

    @room_bp.route("/")
    def list_rooms():
        return json.dumps(registry.list_all_rooms())

    @room_bp.route("/<room_name>", methods=["GET"])
    def list_lights_in_room(room_name):
        room: Room = registry.get_room(room_name)
        attached_lights = list(room.attached_lights.keys())
        result = {
            "name": room.name,
            "attached_lights": attached_lights,
            "grid": json.dumps(room.grid, cls=MyEncoder)
        }
        return json.dumps(result)

    @room_bp.route("/create/<room_name>", methods=["POST"])
    def create_room(room_name):
        #light_controller.list_devices()
        #time.sleep(.5)
        body = request.json
        new_room = registry.create_empty_room(room_name)
        return "OK"

    @room_bp.route("/<room_name>/set_color", methods=["POST"])
    def set_room_color(room_name):
        body = request.json
        r = body['r']
        g = body['g']
        b = body['b']
        room: Room = registry.get_room(room_name)
        if room is None:
            return "ERROR"
        else:
            room.set_all(r, g, b)
            return "OK"
    
    @room_bp.route("/<room_name>/add_light", methods=["POST"])
    def add_light_to_room(room_name):
        body = request.json
        light_id = body['light_id']
        x = body['x']
        y = body['y']

        light = light_registry.get_light_device(light_id)
        room: Room = registry.get_room(room_name)

        if room is None:
            return "ERROR"
        else:
            room.add_light(light, y, x)
            return "OK"
    
    app.register_blueprint(room_bp, url_prefix="/rooms")

