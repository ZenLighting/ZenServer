import socket
from typing import List
from server.model.light_update import LightUpdate
from server.model.sqlmodel import Light
import struct

class LightCommunicator(object):

    def __init__(self, com_socket: socket.socket):
        self.socket = com_socket

    @staticmethod
    def create_header(device_id, opcode, flags, data_length):
        header = struct.pack("!BIIH", device_id, opcode, flags, data_length)
        return header

    def write_update_message(self, light: Light, device_id: int, light_updates: List[LightUpdate]):
        opcode = 0
        header = self.create_header(device_id, opcode, 0, len(light_updates)*4)
        data = b''
        for light_update in light_updates:
            data += struct.pack("!BBBB", light_update.index, light_update.r, light_update.g, light_update.b)

        self.socket.sendto(header+data, (light.address, light.port))