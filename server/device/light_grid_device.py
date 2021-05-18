import abc
from typing import List, Dict


class LightSpotObject(object):
    r: int
    g: int
    b: int

    def set(self, r, g, b):
        pass

class RealLightSpotObject(object):
    r: int
    g: int
    b: int

    def __init__(self, device_id: str, strip_index: int):
        self.parent_device_id = device_id
        self.strip_index = strip_index
        self.updated = False
        self.r = 0
        self.g = 0
        self.b = 0

    def set(self, r, g, b):
        if r != self.r or b != self.b or g != self.g:
            self.updated = True
        self.r = r
        self.g = g
        self.b = b

class BaseLightGrid(abc.ABC):
    @abc.abstractmethod
    def set_light_by_position(self, x, y, r, g, b):
        pass


class LightGridLight(BaseLightGrid):

    def __init__(self, device_id: str, light_map:str = None):
        self.state: List[List[LightSpotObject]] = []
        self.lights_by_index: Dict[int, RealLightSpotObject] = {}
        self.device_id = device_id

        self.updated_flag = False

        if light_map is not None:
            # can imply grid_x and grid_y
            # parse config string
            light_lines = light_map.splitlines()
            current_light_index = 0
            for line in light_lines:
                # for y
                light_row: List[LightSpotObject] = []
                for light_spot in line:
                    # either x or . (x is light, period is space)
                    if light_spot == ".":
                        light_row.append(LightSpotObject())
                    else:
                        real_light = RealLightSpotObject(self.device_id, current_light_index)
                        self.lights_by_index[current_light_index] = real_light
                        light_row.append(real_light)
                        current_light_index += 1
                self.state.append(light_row)

    def set_light_by_index(self, index, r, g, b):
        print(index)
        light = self.lights_by_index.get(index)
        if light.r != r or light.g != g or light.b != b:
            self.updated_flag = True
        self.lights_by_index.get(index).set(r, g, b)
        #self.updated_flag = True

    def set_light_by_position(self, x, y, r, g ,b):
        if self.state[y][x].r != r or self.state[y][x] != g or self.state[y][x] != b:
            self.updated_flag = True
        self.state[y][x].set(r, g, b)

    def set_all(self, r, g, b):
        for light in self.lights_by_index.values():
            light.set(r, g, b)
            if light.updated:
                self.updated_flag = True

    def compile_updated_lights(self, set_flag=False) -> List[RealLightSpotObject]:
        lights_updated = []
        for light in self.lights_by_index.values():
            if light.updated:
                lights_updated.append(light)
        return lights_updated

