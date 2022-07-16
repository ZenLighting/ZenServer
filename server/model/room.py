from typing import List, Tuple
import pydantic
from server.model.grid import LightGrid, LightGridEvents
from server.model.light import LightDeviceWrapper
from server.model.sqlite_models import RoomModel

class LightPositionDescriptor(object):
    def __init__(self, x:int, y:int, light: LightDeviceWrapper):
        self.x = x
        self.y = y
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
            self.grid.transpose_grid(light_position.light.grid_object, (light_position.x, light_position.y), True)

    def set_room_color(self, r, g, b):
        # makes sure all light grids are notified of changes to color
        self.grid.set_grid_color(r, g, b)
        for light_pos in self.lights:
            light_pos.light.grid_object.trigger_event(LightGridEvents.GRID_CHANGE)
        
    def json(self):
        lights_as_json = []
        for light in self.lights:
            as_json = {
                "x": light.x,
                "y": light.y,
                "light": light.light.model_object.dict(exclude={"rooms": True})
            }
            lights_as_json.append(as_json)
        return {
            "model": self.model.dict(exclude={"lights": True}),
            "grid": str(self.grid),
            "lights": lights_as_json
        }
    

