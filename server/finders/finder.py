import socket
import threading
import struct

class DeviceFinder(threading.Thread):

    def __init__(self, broadcast_socket=None):
        self.broadcast_recv_socket = broadcast_socket
        self.exit_flag = False

        if self.broadcast_recv_socket is None:
            self.init_socket()        

    def init_socket(self):
        self.broadcast_recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        self.broadcast_recv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.broadcast_recv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.broadcast_recv_socket.settimeout(1)
        self.broadcast_recv_socket.bind(("", 2000))
    
    def run(self):
        while not self.exit_flag:
            message, addr = self.broadcast_recv_socket.recvfrom(1024)
            if message is not None:
                # a valid message was received
                uuid, opcode, flags, striplen = struct.unpack("!16sIII", message)
                # check if the light device already exists
                # check if the device 
