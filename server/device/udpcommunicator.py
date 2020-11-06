from server.device.abccommunicator import ABCCommunicator
import socket
import struct

class UDPCommunicator(ABCCommunicator):

    def __init__(self, state_manager, address):
        super().__init__(state_manager)
        self.address = address
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(("", 0))

    def generate_message(self, brightness: int, state: list):
        message = self.state_manager.get_token() # 16 bytes
        message += struct.pack("!B", brightness) # 1 byte
        for (r, g, b) in state:
            message += struct.pack("!BBB", r, g, b)
        return message

    def send_frame(self, brightness: int, state: list):
        message = self.generate_message(brightness, state)
        self.socket.sendto(message, self.address)
