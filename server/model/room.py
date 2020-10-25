from dataclasses import dataclass
from typing import Dict, List
from server.model.light import LightDevice

class Room:
    name: str
    grid: List[list]
    attached_lights: Dict[str, {
        "x": str,
        "y": str,
        "light": LightDevice
    }]
