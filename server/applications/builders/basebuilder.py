from typing import Any, Dict
from server.model.grid import LightGrid
from server.applications.application.light_application import LightApplicationTemplate

class LightApplicationBuilder(object):
    def __call__(self, grid_object: LightGrid, args: Dict[str, Any]) -> LightApplicationTemplate:
        raise(NotImplementedError())

