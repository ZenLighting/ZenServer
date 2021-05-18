from sys import float_repr_style
from sqlalchemy.sql.expression import update
from server.model.database import DatabaseSession
from server.model.sql_model import LightDevice, Room
import server.model.sql_model
from server.device.light_grid_device import LightGridLight
from server.mqtt.mqtt_service import MqttService
from typing import Any, Dict
import time
import struct
import threading
from server.device.room import LightObjectParent

class LightManager(object):

    def __init__(self, mqtt_communicator: MqttService):
        self.light_objects: Dict[str, LightGridLight] = {}
        self.rooms: Dict[str, LightObjectParent] = {}
        self.mqtt = mqtt_communicator
        
        self.thread = threading.Thread(target=self.light_update_thread)
        self.thread.start()

        self.update_from_db()

    def update_from_db(self):
        with DatabaseSession() as session:
            # get all the light objects
            lights = session.query(LightDevice).all()
            for light in lights:
                # create light state manager
                new_light = LightGridLight(light.device_id, light.light_mapping)
                self.light_objects[light.device_id] = new_light
                #TODO connect lights to rooms
                if light.room != None:
                    # check if room exists
                    room = self.rooms.get(light.room)
                    room_db = session.query(Room).filter(Room.id==light.room).one()
                    if room is None:
                        new_room = LightObjectParent(name=room_db.room_name, id=room_db.id)
                        self.rooms[light.room] = new_room
                        room = new_room
                        print(f"Created room {new_room.id}:{new_room.name}")
                    room.add_light_to_room(light.room_x, light.room_y, new_light)

    def light_update_thread(self):
        print("starting update thread")
        while True:
            for light_id in self.light_objects:
                light_object = self.light_objects[light_id]
                if light_object.updated_flag:
                    # this light has been updated
                    # compile message to light
                    updated_lights = light_object.compile_updated_lights(True)
                    # format message
                    data = b''
                    for light in updated_lights:
                        data += struct.pack("<BBBB", light.strip_index, light.r, light.g, light.b)
                    header = struct.pack("<BIIH", 0, 0, 0, len(data))
                    # send message
                    self.mqtt.client.publish(f"device/{light_id}/input", header+data)
                    # reset update flag so this update is not sent again
                    light_object.updated_flag = False
                    print("updated light")
            time.sleep(1/30)