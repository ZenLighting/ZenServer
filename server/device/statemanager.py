from server.model.grid import NeoPixel, GridSpace
import math

class StateManager(object):

    def __init__(self, light_grid: str):
        self.grid, self.light_dict = self.parse_grid_string(light_grid)
        self.brightness = 255
        self.light_keys = list(self.light_dict.keys())
        self.max_index = max(self.light_keys)+1
        self.token = b'0000000000000000'

    def set_token(self, token: bytes):
        self.token = token

    def get_token(self):
        return self.token

    def get_state(self):
        values = []
        for i in range(self.max_index):
            #print(self.light_dict)
            light: NeoPixel = self.light_dict[i]
            value = (light.r, light.g, light.b)
            values.append(value)
        return self.brightness, values

    def set_index(self, x, y, r, g, b):
        neopixel = self.grid[x][y]
        if isinstance(neopixel, NeoPixel):
            neopixel: NeoPixel
            neopixel.r = r
            neopixel.g = g
            neopixel.b = b
    
    def set_row(self, row, r, g, b):
        for i in range(len(self.grid[row])):
            pixel = self.grid[row][i]
            if isinstance(pixel, NeoPixel):
                pixel: NeoPixel
                pixel.r = r
                pixel.g = g
                pixel.b = b

    def set_col(self, col, r, g, b):
        for i in range(len(self.grid)):
            pixel = self.grid[i][col]
            if isinstance(pixel, NeoPixel):
                pixel: NeoPixel
                pixel.r = r
                pixel.g = g
                pixel.b = b

    def set_all(self, r, g, b):
        for neopixel in self.light_dict.values():
            neopixel: NeoPixel
            neopixel.r = r
            neopixel.g = g
            neopixel.b = b

    def set_brightness(self, brighness: int):
        self.brightness = brighness
    
    
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
                    neopixel_dict[index] = new_grid_space
                else:
                    new_grid_space = 0 #GridSpace()
                row.append(new_grid_space)
            end_result.append(row)
        return end_result, neopixel_dict