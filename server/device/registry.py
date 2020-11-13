from server.model.light import LightDevice

class DeviceRegistry(object):

    def __init__(self):
        self.device_identifiers = set()
        self.devices = {}

    def check_device_exists(self, device_identifier):
        if device_identifier in self.device_identifiers:
            return True
        else:
            return False

    def add_light_device(self, device: LightDevice):
        self.device_identifiers.add(device.light_id)
        self.devices[device.light_id] = device
        print(self.devices)

    def get_light_device(self, device_identifier):
        return self.devices.get(device_identifier)