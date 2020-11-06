from dataclasses import dataclass
from server.model.light import LightDevice

@dataclass
class UDPLightDevice(LightDevice):
    address: str
    port: str

    
