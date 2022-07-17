from typing import List
#from server.model.light import LightDevice
from server.model.sqlite_models import LightDeviceORM, LightDeviceModel, PartialDevice, RoomLightAssociation
from server.model.light import LightDeviceWrapper
from sqlalchemy.orm.session import sessionmaker, Session
from typing import Dict
from server.model.room import LightPositionDescriptor, RoomWrapper#, RoomModel
from server.model.sqlite_models import RoomModel, RoomOrm
from server.device.registry import DeviceRegistry

class RoomRegistry(object):
    def __init__(self, session_maker: sessionmaker, light_registry: DeviceRegistry):
        self.database_session_maker = session_maker
        self.device_registry = light_registry
        #self.devices = {}
        ## =========== deleteme

        self.rooms: List[RoomWrapper] = self.generate_rooms_from_database(session_maker)

    def generate_rooms_from_database(self, session_maker):
        session: Session = session_maker()
        room_orms: List[RoomOrm] = session.query(RoomOrm).all()
        room_wrappers = []
        for room in room_orms:
            as_model = RoomModel.from_orm(room)
            print(room.lights)
            light_wrappers_with_position = []
            for light_orm_assoc in room.lights:
                light_wrapper = self.device_registry.get_light_device(light_orm_assoc.light.id)
                light_wrappers_with_position.append(LightPositionDescriptor(x=light_orm_assoc.x, y=light_orm_assoc.y, light=light_wrapper))
            new_wrapper = RoomWrapper(as_model, light_wrappers_with_position)
            room_wrappers.append(new_wrapper)
            #wrapped = RoomWrapper(as_model)
            #light_wrappers.append(wrapped)
        session.close()
        return room_wrappers

    def add_room(self, room_model: RoomModel):
        wrapped = RoomWrapper(room_model, []) # start with no lights in room
        session: Session = self.database_session_maker()
        new_sql_room = RoomOrm()
        new_sql_room.name = room_model.name
        session.add(new_sql_room)
        session.commit()
        self.rooms.append(wrapped)
        session.close()
        return wrapped

    def remove_room(self, room_model: RoomModel):
        # remove from database
        session: Session = self.database_session_maker()
        room = session.query(RoomOrm).filter(RoomOrm.name==room_model.name).one()
        session.delete(room)
        session.commit()
        # remove from the array
        for i, room in enumerate(self.rooms):
            if room.model.name == room_model.name:
                self.rooms.pop(i)
                break
        session.close()
    
    def add_light_to_room(self, light: LightDeviceModel, room: RoomModel, x: int, y: int):
        # add light to database
        session: Session = self.database_session_maker()
        light = session.query(LightDeviceORM).filter(LightDeviceORM.id == light.id).one()
        room = session.query(RoomOrm).filter(RoomOrm.name == room.name).one()
        association = RoomLightAssociation()
        association.x = x
        association.y = y
        association.room = room
        association.light = light
        room.lights.append(association)
        light.rooms.append(association)
        session.add(association)
        session.commit()

    def get_room(self, room_name: str):
        for room in self.rooms:
            if room.model.name == room_name:
                return room
        raise(Exception("Room not found"))




    """def check_device_exists(self, device_identifier):
        if self.get_light_device(device_identifier) is not None:
            return True
        else:
            return False

    def check_partial_exists(self, device_name: str):
        if self.undefinedDevices.get(device_name) is None:
            return False
        return True

    def add_partial_device(self, device: PartialDevice):
        self.undefinedDevices[device.name] = device

    def add_light_device(self, device: LightDeviceModel):
        wrapped = LightDeviceWrapper(device)
        self.devices.append(wrapped)
        session: Session = self.database_session_maker()
        new_sql_device = LightDeviceORM()
        new_sql_device.grid_string = device.grid_string
        new_sql_device.name = device.name
        new_sql_device.last_address = device.last_address
        session.add(new_sql_device)
        session.commit()
        device.id = new_sql_device.id
        session.close()

    def get_light_device(self, device_identifier, name=None):
        for deviceWrapper in self.devices:
            if name:
                if deviceWrapper.model_object.name == name:
                    return deviceWrapper
            else:
                if deviceWrapper.model_object.id == device_identifier:
                    return deviceWrapper
        return None"""

    """def list_registered_macs(self):
        return list(self.device_identifiers)"""