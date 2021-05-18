from typing import List, Dict
import server.device.light_grid_device as grid_device

class LightObjectParent(grid_device.BaseLightGrid):

    def __init__(self, name, id, initial_x=1, initial_y=1):
        self.name = name
        self.id = id
        self.state: List[List[grid_device.LightSpotObject]] = []
        self.light_positions: Dict[str, dict] = {}
        self.light_objects: Dict[str, grid_device.LightGridLight] = {}

        self.expand_grid(initial_x, initial_y)

    @property
    def size_x(self):
        return len(self.state[0])

    @property
    def size_y(self):
        return len(self.state)

    def expand_grid(self, new_x: int, new_y: int):
        new_state = []
        # create new grid
        for i in range(new_y):
            new_row = []
            for u in range(new_x):
                new_row.append(grid_device.LightSpotObject())
            new_state.append(new_row)
        # transfer over the old state
        for y, row in enumerate(self.state):
            for x, light in enumerate(row):
                # no need to add lights if they are empty fillers
                if isinstance(light, grid_device.RealLightSpotObject):
                    new_state[y][x] = light
        
        self.state = new_state

    def set_light_by_position(self, x, y, r, g, b):
        light_object = self.state[y][x]
        if isinstance(light_object, grid_device.RealLightSpotObject):
            # this is a real light
            light_object: grid_device.RealLightSpotObject
            light_parent_id = light_object.parent_device_id
            light_index = light_object.strip_index
            light_parent = self.light_objects.get(light_parent_id)
            light_parent.set_light_by_index(light_index, r, g, b)

    def set_all_lights(self, r, g, b):
        for row in self.state:
            for light in row:
                if isinstance(light, grid_device.RealLightSpotObject):
                    light: grid_device.RealLightSpotObject
                    light_parent_id = light.parent_device_id
                    light_index = light.strip_index
                    light_parent = self.light_objects.get(light_parent_id)
                    light_parent.set_light_by_index(light_index, r, g, b)

                #light.set(r, g, b)
    def add_light_to_room(self, x, y, light: grid_device.LightGridLight):
        # calculate if we have enough room
        light_rows = len(light.state)
        light_cols = len(light.state[0])

        if light_rows + y >= len(self.state):
            # we dont have enough rows
            self.expand_grid(self.size_x, light_rows + y)

        if light_cols + x >= len(self.state[0]):
            # we dont have enough columns
            self.expand_grid(light_cols+x, self.size_y)

        # add light to management
        self.light_positions[light.device_id] = {
            "x": x,
            "y": y
        }
        self.light_objects[light.device_id] = light

        for y_internal, row in enumerate(light.state):
            for x_internal, individual_light in enumerate(row):
                self.state[y+y_internal][x+x_internal] = individual_light
        



