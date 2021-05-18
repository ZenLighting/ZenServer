from server.device.room import LightObjectParent
from flask import Blueprint, Flask, request
#from server.controllers.device_controller import DeviceController 
from server.device.registry import DeviceRegistry
#from server.rooms.room import Room
#from server.rooms.roomRegistry import RoomRegistry
#from server.model.light import DeviceEncoder
#from server.hub.server import LightServer
import json
import time
from server.device.light_device_manager import LightManager
from server.model.database import DatabaseSession
import server.model.sql_model as Model
from server.device.room import LightObjectParent

class MyEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__    

def attach_blueprint(app: Flask):
    container = app.container
    #light_registry: DeviceRegistry = container.device_registry
    state_manager: LightManager = container.light_state_manager

    room_bp = Blueprint("room", __name__)

    @room_bp.route("/")
    def list_rooms():
        with DatabaseSession() as session:
            rooms = session.query(Model.Room).all()
        return {
            "status": 200,
            "data": list(map(lambda x: x.__dict__, rooms))
        }

    @room_bp.route("/<room_name>", methods=["GET"])
    def list_lights_in_room(room_name):
        with DatabaseSession() as session:
            room = session.query(Model.Room).filter(Model.Room.room_name==room_name).one()
        print(state_manager.rooms)
        room_statefull: LightObjectParent = state_manager.rooms.get(str(room.id))
        #attached_lights = list(room.attached_lights.keys())
        result = {
            "name": room.room_name,
            "attached_lights": list(room_statefull.light_objects.keys()),
            "grid": json.dumps(room_statefull.state, cls=MyEncoder)
        }
        return {
            "status": 200,
            "data": result
        }

    @room_bp.route("/create/<room_name>", methods=["POST"])
    def create_room(room_name):
        #light_controller.list_devices()
        #time.sleep(.5)
        body = request.json
        with DatabaseSession() as session:
            new_room = Model.Room()
            new_room.room_name = room_name
            session.add(new_room)
            session.commit()
        #
        # new_room = registry.create_empty_room(room_name)
        return {
            "status": 200,
            "data": new_room.__dict__
        }

    @room_bp.route("/<room_name>/set_color", methods=["POST"])
    def set_room_color(room_name):
        body = request.json
        r = body['r']
        g = body['g']
        b = body['b']
        with DatabaseSession() as session:
            room_db = session.query(Model.Room).filter(Model.Room.room_name==room_name).one()
        print(state_manager.rooms)
        room: LightObjectParent= state_manager.rooms.get(str(room_db.id))

        if room is None:
            return {
                "status": 404,
                "data": "room with that name do not exist"
            }
        else:
            room.set_all_lights(r, g, b)
            result = {
                "name": room.name,
                "id": room.id,
                "attached_lights": list(room.light_objects.keys()),
                "grid": json.dumps(room.state, cls=MyEncoder)
            }
            return {
                "status": 200,
                "data": result
            }
    
    @room_bp.route("/<room_name>/add_light", methods=["POST"])
    def add_light_to_room(room_name):
        body = request.json
        light_id = body['light_id']
        x = body['x']
        y = body['y']

        with DatabaseSession() as session:
            room = session.query(Model.Room).filter(Model.Room.room_name==room_name).one()
            light = session.query(Model.LightDevice).filter(Model.LightDevice.device_id==light_id).one()
            light.room = room.id
            light.room_x = x
            light.room_y = y
            session.commit()
        
        state_manager.update_from_db()

        if room is None:
            return {
                "status": 400,
                "data": "room did not exist"
            }
        else:
            return {
                "status": 200,
                "data": {
                    "light_model": light,
                    "light_state": state_manager.light_objects.get(light.device_id).state
                }
            }
    
    app.register_blueprint(room_bp, url_prefix="/rooms")

