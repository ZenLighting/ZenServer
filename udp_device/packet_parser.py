import struct
from udp_device.udp_device import UDPLightDevice
import json

class PacketParser(object):

    @staticmethod
    def parse_register_message(self, udp_data: bytes) -> UDPLightDevice:
        