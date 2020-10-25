from dataclasses import dataclass
from typing import List, Tuple, Dict
from dataclasses_json import dataclass_json
from json import JSONEncoder


@dataclass_json
@dataclass
class GridSpace(object):
    pass

@dataclass_json
@dataclass
class NeoPixel(GridSpace):
    index: Tuple[int, int]
    r: int
    g: int
    b: int

@dataclass_json
@dataclass
class LightDevice(object):
    light_id: int
    num_leds: int
    brightness: int
    light_grid: List[List[GridSpace]]
    neopixel_list: Dict[int, NeoPixel]
    active: bool = True

    

class DeviceEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

