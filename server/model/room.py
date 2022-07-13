from typing import List, Tuple
import pydantic
from server.model.grid import LightGrid
from server.model.light import LightDeviceWrapper

class RoomModel(object):
    name: str

class LightPositionDescriptor(object):
    def __init__(self, position: Tuple[int, int], light: LightDeviceWrapper):
        self.position = position
        self.light = light

class RoomWrapper(object):
    model: RoomModel
    grid: LightGrid
    lights: List[LightPositionDescriptor]

    def __init__(self, model, lights: List[LightPositionDescriptor]):
        self.model = model
        self.lights = lights
        self.grid = LightGrid("000")
        self._place_lights_onto_grid()

    def _place_lights_onto_grid(self):
        for light_position in self.lights:
            self.grid.transpose_grid(light_position.light.grid_object, light_position.position, True)

