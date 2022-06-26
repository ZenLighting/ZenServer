from dataclasses import dataclass
from inspect import Parameter
from typing import List, Tuple, Dict, Any, Optional
#from server.device.statemanager import StateManager
import pydantic

"""@dataclass
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
        return "[{:02d}]{:03d}:{:03d}:{:03d}".format(self.index, self.r, self.g, self.b)"""

class GridSpace(object):
    index: int = -1
    r: int = -1
    g: int = -1
    b: int = -1
    light_pointer: Optional[Any] = None

    def set_color(self, r, g, b):
        return False

    def __str__(self):
        return "(---,---,---)"

class PixelGridSpace(GridSpace):
    def __init__(self, index, r=0, g=0, b=0):
        self.index = index
        self.r = 0
        self.g = 0
        self.b = 0

    def set_color(self, r, g, b):
        toReturn = False
        if r != self.r or g != self.g or b != self.b:
            toReturn = True
        self.r = r
        self.b = b
        self.g = g
        return toReturn
    
    def __str__(self):
        return f"({str(self.r).zfill(3)},{str(self.g).zfill(3)},{str(self.b).zfill(3)})"

class LightGrid(object):
    grid_object: List[List[GridSpace]]
    pixels_by_index = List[PixelGridSpace]

    def __init__(self, light_grid_string: str): # rooms can be defined by grid strings of only -
        self._grid_setup_string = light_grid_string
        self.grid_object, self.pixels_by_index = self.parse_light_grid_string(light_grid_string)
        for pixel in self.pixels_by_index:
            pixel.light_pointer = self

    def transpose_grid(self, other_grid, start_coords: Tuple[int, int], expand=False):
        my_needed_size_x = start_coords[0]+other_grid.grid_x
        my_needed_size_y = start_coords[1]+other_grid.grid_y
        print(self.grid_x, self.grid_y)
        # check if we need to change the size of the grid
        if self.grid_x < my_needed_size_x:
            needed_x_expansion = my_needed_size_x - self.grid_x
            # we need to expand gri
            if not expand:
                raise(Exception("Cannot transpose, grid does not meet requirements in x directions"))
            # expand the grid
            for row in self.grid_object:
                row.extend([GridSpace()]*needed_x_expansion)
        if self.grid_y < my_needed_size_y:
            needed_y_expansion = my_needed_size_y - self.grid_y
            if not expand:
                raise(Exception("Cannot transpose, grid does not meet requirements in y direction"))
            
            for i in range(needed_y_expansion):
                self.grid_object.append([GridSpace()]*my_needed_size_x)

        print(self.grid_x, self.grid_y)
        # perform the actual transpose
        for i, row in enumerate(other_grid.grid_object):
            for u, col in enumerate(row):
                print(i+start_coords[1],i+start_coords[1])
                if isinstance(col, PixelGridSpace): 
                    self.grid_object[i+start_coords[1]][u+start_coords[0]] = col
        
        # repopulate the pixels_by_index array
        self.pixels_by_index = []
        for row in self.grid_object:
            for col in row:
                if isinstance(col, PixelGridSpace):
                    self.pixels_by_index.append(col)
        return


    @property
    def grid_x(self):
        return len(self.grid_object[0])
    
    @property
    def grid_y(self):
        return len(self.grid_object)

    @property
    def num_leds(self):
        return len(self.pixels_by_index)

    @staticmethod
    def parse_light_grid_string(light_grid_string: str) -> Tuple[List[List[GridSpace]], List[PixelGridSpace]]:
        light_grid_string = light_grid_string.rstrip("\n")
        light_grid_rows = light_grid_string.split('\n')
        light_index = 0
        
        grid_object: List[List[GridSpace]] = []
        pixels_list: List[PixelGridSpace] = []

        for row in light_grid_rows:
            row_array = list()
            for charecter in row:
                if charecter == "-":
                    row_array.append(GridSpace())
                    continue
                else:
                    new_pixel_gridspace = PixelGridSpace(
                        index = light_index,
                        r = 0,
                        g = 0,
                        b = 0
                    )
                    light_index += 1
                    row_array.append(new_pixel_gridspace)
                    pixels_list.append(new_pixel_gridspace)
            grid_object.append(row_array)
        return grid_object, pixels_list

    
    def set_index_color(self, row, col ,r ,g ,b):
        pixel = self.grid_object[row][col]
        if isinstance(pixel, PixelGridSpace):
            return pixel.set_color(r, g, b)
        return False

    def __str__(self):
        stringrep = ""
        for row in self.grid_object:
            for col in row:
                stringrep+=str(col)
            stringrep+="\n"
        return stringrep