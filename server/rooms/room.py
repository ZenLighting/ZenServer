from dataclasses import dataclass
from typing import Dict, List
from server.model.light import LightDevice
from server.model.grid import GridSpace, NeoPixel
from typing import TypedDict

class LightLocationObject(TypedDict):
    x: int
    y: int
    light: LightDevice


class Room:
    name: str
    grid: List[list]
    attached_lights: Dict[str, LightLocationObject]

    def __init__(self, name):
        self.name = name
        self.grid = []
        self.attached_lights = {}

    def add_light(self, light: LightDevice, row: int, col: int):
        # check dimensions of the existing grid see if it will work
        light_rows = len(light.light_grid)
        light_cols = len(light.light_grid[0])

        required_rows = row + light_rows
        required_cols = col + light_cols

        # extend 
        grid_rows = len(self.grid)
        grid_cols = 0
        row_dif = required_rows - grid_rows
        col_dif = required_cols
        if grid_rows > 0:
            grid_cols = len(self.grid[0])
            col_dif = col_dif - grid_cols

        # extend existing columns
        for grid_row in self.grid:
            grid_row.extend([0]*col_dif)

        #add new rows with correct amount of columns    
        if row_dif > 0:
            for i in range(row_dif):
                self.grid.append([0]*required_cols)
        
        #TODO check for conflicts with exisiting lights

        # transpose light grid onto room grid
        for light_row_i in range(len(light.light_grid)):
            for light_col_i in range(len(light.light_grid[light_row_i])):
                self.grid[light_row_i+row][light_col_i+col] = light.state.grid[light_row_i][light_col_i]
                #print("room:[{}, {}] light_grid:[{}, {}]-> id:{}=id:{}".format(light_row_i+row, light_col_i+col, light_row_i, light_col_i, id(self.grid[light_row_i+row][light_col_i+col]), id(light.light_grid[light_row_i][light_col_i])))
                #print(id(light.light_grid[light_row_i][light_col_i]), id(self.grid[light_row_i+row][light_col_i+col]))
                #print("ASD")
        # add light to mapping
        self.attached_lights[light.light_id] = {
            "x": col,
            "y": row,
            "light": light
        }

    def set_all(self, r, g, b):
        for row in self.grid:
            for item in row:
                if isinstance(item, NeoPixel):
                    item: NeoPixel
                    item.r = r
                    item.g = g
                    item.b = b

    def set_row(self, row, r, g, b):
        row = self.grid[row]
        for item in row:
            if isinstance(item, NeoPixel):
                item: NeoPixel
                item.r = r
                item.g = g
                item.b = b
    
    def set_col(self, col, r, g, b):
        for row in self.grid:
            item = row[col]
            if isinstance(item, NeoPixel):
                item: NeoPixel
                item.r = r
                item.g = g
                item.b = b
    