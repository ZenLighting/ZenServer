from flask import Blueprint, Flask, request, Response
#from server.controllers.device_controller import DeviceController 
from server.device.registry import DeviceRegistry
from server.device.room_registry import RoomRegistry
#from server.model.light import DeviceEncoder
#from server.hub.server import LightServer
import json
import time
from server.model.requests.rooms import AddLightToRoomPOST, SetRoomColorPOST

from server.model.sqlite_models import LightDeviceModel, RoomModel

"""not valid at the moment, not for version 1"""

class MyEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__    

def create_blueprint(registry: RoomRegistry, light_registry: DeviceRegistry):
    room_bp = Blueprint("room", __name__)

    @room_bp.route("/", methods=["GET"])
    def list_rooms():
        as_serializable_list = list(map(lambda x: x.json(), registry.rooms))
        return {
            "rooms": as_serializable_list
        }
        #return json.dumps(registry.list_all_rooms())

    """@room_bp.route("/<room_name>", methods=["GET"])
    def list_lights_in_room(room_name):
        room: Room = registry.get_room(room_name)
        attached_lights = list(room.attached_lights.keys())
        result = {
            "name": room.name,
            "attached_lights": attached_lights,
            "grid": json.dumps(room.grid, cls=MyEncoder)
        }
        return json.dumps(result)"""

    @room_bp.route("/", methods=["POST"])
    def create_room():
        #light_controller.list_devices()
        #time.sleep(.5)
        #print("HERE")
        body = request.json
        room_model = RoomModel.parse_obj(body)
        new_room = registry.add_room(room_model)
        return "OK"

    @room_bp.route("/<room_name>", methods=["GET"])
    def get_room(room_name):
        for i in registry.rooms:
            if i.model.name == room_name:
                return {
                    "room": i.json()
                }
        return Response("Room does not exist", status=404)

    @room_bp.route("/<room_name>", methods=["DELETE"])
    def delete_room(room_name):
        room_model = RoomModel(name=room_name)
        registry.remove_room(room_model)
        return "OK"

    @room_bp.route("/<room_name>/add_light", methods=["POST"])
    def add_light_to_room(room_name):
        body = request.json
        add_light_request = AddLightToRoomPOST.parse_obj(body)
        room_model = RoomModel(name=room_name)
        fake_light_model = LightDeviceModel(id=add_light_request.light, name="", grid_string="")
        registry.add_light_to_room(fake_light_model, room_model, add_light_request.x, add_light_request.y)
        return "OK"

    @room_bp.route("/<room_name>/set_color", methods=["POST"])
    def set_room_color(room_name):
        body = request.json
        set_color_request = SetRoomColorPOST.parse_obj(body)
        room = registry.get_room(room_name)
        room.set_room_color(set_color_request.r, set_color_request.g, set_color_request.b)
        return "OK"

    """@room_bp.route("/<room_name>/add_light", methods=["POST"])
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
            return "OK"""
    return room_bp
    
    app.register_blueprint(room_bp, url_prefix="/rooms")

