from server.model.light import LightDevice, NeoPixel, GridSpace
import logging
from typing import Dict

log = logging.getLogger(__name__)

class LightRegistry(object):

    def __init__(self):
        self.connected_lights: Dict[int, LightDevice] = {}
        self.light_hashes = set()

    def register_light(self, light_id: int, led_number: int, light_grid: str):
        light_hash = str(light_id)+str(led_number)+light_grid
        if light_hash not in self.light_hashes:
            grid, neo_dict = self.parse_grid_string(light_grid)
            self.connected_lights[light_id] = LightDevice(light_id, led_number, 255, grid, neo_dict)
            log.info(f"Registered device {light_id}, {self.connected_lights[light_id]}")
        return self.connected_lights[light_id]
    
    @staticmethod
    def parse_grid_string(grid_string: str):
        lines = grid_string.splitlines()
        end_result = []
        neopixel_dict = {}
        for line in lines:
            values = line.split(" ")
            row = []
            for value in values:
                if value != ".":
                    index = int(value)
                    new_grid_space = NeoPixel(index, 0, 0, 0)
                    neopixel_dict[index] = NeoPixel
                else:
                    new_grid_space = GridSpace()
                row.append(new_grid_space)
            end_result.append(row)
        return end_result, neopixel_dict


