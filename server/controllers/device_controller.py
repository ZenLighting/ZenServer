from server.hub.server import LightServer
from server.hub.registry import LightRegistry
from server.model.light import LightDevice
import time
import json
from json import JSONEncoder

class DeviceController(object):

    def __init__(self, device_server: LightServer, device_registry: LightRegistry):
        self.server = device_server
        self.registry = device_registry

    def list_devices(self):
        self.server.gather_lights()
        time.sleep(.5)
        light_map = self.registry.connected_lights
        device_list = []
        for uuid in light_map:
            light_json = {}
            light_obj: LightDevice = light_map[uuid]
            light_json = {
                "id": light_obj.light_id,
                "grid": light_obj.light_grid,
                "num_leds": light_obj.num_leds
            }
            device_list.append(light_json)
        return device_list