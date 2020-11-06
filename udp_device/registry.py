from server.model.light import LightDevice

class UDPDeviceRegistry(object):

    def __init__(self):
        self.light_to_addr_map = {}
        self.id_to_light_map = {}

    def add_light(address: tuple,):
        self.light_to_addr_map[device] = 