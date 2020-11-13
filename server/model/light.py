from dataclasses import dataclass
from typing import List, Tuple, Dict, Any
from json import JSONEncoder
from server.device.abccommunicator import ABCCommunicator
from server.model.grid import GridSpace, NeoPixel
from server.device.statemanager import StateManager

@dataclass
class LightDevice(object):
    light_id: int
    num_leds: int
    brightness: int
    light_grid: List[List[GridSpace]]
    neopixel_list: Dict[int, NeoPixel]
    state: Any#: StateManager
    communicator: Any#: ABCCommunicator
    active: bool = True

    

class DeviceEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

