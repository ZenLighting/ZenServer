from datetime import datetime
import socket
from typing import List
from server.device.registry import DeviceRegistry
import time
from pydantic import BaseModel
from server.model.light import LightDeviceWrapper
from server.model.sqlite_models import PartialDevice

class StripDescription(BaseModel):
    length: int

class CommunicationDescription(BaseModel):
    protocols: List[int]

class LightBroadcastMessage(BaseModel):
    """{
        "name": "Device name",
        "strip": {
            "length": -999
        },
        "communication": {
            "protocols": [0, 1, 2]
        }
    }"""
    name: str
    strip: StripDescription
    communication: CommunicationDescription


class DeviceHeartbeatDetector(object):

    def __init__(self, device_registry: DeviceRegistry,  device_protocol_disc_port=1260):
        self.device_registry = device_registry
        self.sockfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        self.sockfd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sockfd.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sockfd.setblocking(True)
        self.sockfd.bind(('', device_protocol_disc_port))

    def run(self):
        while True:
            data, address = self.sockfd.recvfrom(1024) # messages should be
            dataParsed = LightBroadcastMessage.parse_raw(data)
            device = self.device_registry.get_light_device(None, name=dataParsed.name)
            if device is None:
                # the device is not in the database
                #if not self.device_registry.check_partial_exists()
                print("Unknown Device Heartbeat", data)
                partial_device = PartialDevice(name=dataParsed.name, last_address=address[0])
                self.device_registry.add_partial_device(partial_device)
            else:
                device: LightDeviceWrapper
                device.model_object.last_address = address[0]
                device.heartbeat = datetime.now()
            time.sleep(0) # makes compatable with green threads