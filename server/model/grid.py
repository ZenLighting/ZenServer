from dataclasses import dataclass
from typing import List, Tuple, Dict, Any
#from server.device.statemanager import StateManager

@dataclass
class GridSpace(object):
    def __str__(self):
        return "[--]---:---:---"

@dataclass
class NeoPixel(GridSpace):
    index: int
    r: int
    g: int
    b: int

    def __str__(self):
        return "[{:02d}]{:03d}:{:03d}:{:03d}".format(self.index, self.r, self.g, self.b)