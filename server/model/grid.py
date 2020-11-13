from dataclasses import dataclass
from typing import List, Tuple, Dict, Any
#from server.device.statemanager import StateManager

@dataclass
class GridSpace(object):
    pass

@dataclass
class NeoPixel(GridSpace):
    index: Tuple[int, int]
    r: int
    g: int
    b: int