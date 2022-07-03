from typing import List
#from server.model.light import LightDevice
from server.model.sqlite_models import LightDeviceORM, LightDeviceModel
from server.model.light import LightDeviceWrapper
from sqlalchemy.orm.session import sessionmaker, Session

class DeviceRegistry(object):

    def __init__(self, session_maker: sessionmaker):
        self.database_session_maker = session_maker
        self.device_identifiers = set()
        #self.devices = {}
        ## =========== deleteme

        self.devices: List[LightDeviceWrapper] = self.generate_device_from_database(session_maker)

    def generate_device_from_database(self, session_maker):
        session: Session = session_maker()
        light_devices = session.query(LightDeviceORM).all()
        light_wrappers = []
        for device in light_devices:
            as_model = LightDeviceModel.from_orm(device)
            wrapped = LightDeviceWrapper(as_model)
            light_wrappers.append(wrapped)
        session.close()
        return light_wrappers

    def check_device_exists(self, device_identifier):
        if self.get_light_device(device_identifier) is not None:
            return True
        else:
            return False

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
        return None

    """def list_registered_macs(self):
        return list(self.device_identifiers)"""