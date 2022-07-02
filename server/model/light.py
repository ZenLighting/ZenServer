from dataclasses import dataclass
from typing import List, Tuple, Dict, Any
from server.model.grid import LightGrid
from server.model.sqlite_models import LightDeviceModel
from server.device.device_grid_writer import DeviceGridWriter
from datetime import datetime


class LightDeviceWrapper(object):
    model_object: LightDeviceModel
    grid_object: LightGrid
    deviceStateCom: DeviceGridWriter
    heartbeat: datetime = None

    def __init__(self, model):
        self.model_object = model
        self.grid_object = LightGrid(self.model_object.grid_string)
        self.deviceStateCom = DeviceGridWriter(self.model_object, self.grid_object)