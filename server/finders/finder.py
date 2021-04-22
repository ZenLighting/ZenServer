import socket
import threading
import struct
from server.model.sqlmodel import Light
from server.finders.light_tracker import LightTracker

class DeviceFinder(threading.Thread):

    def __init__(self, available_light_tracker: LightTracker, broadcast_socket=None):
        threading.Thread.__init__(self)
        self.available_light_tracker = available_light_tracker
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
        header_len = struct.calcsize("!16sIII")
        while not self.exit_flag:
            try:
                message, addr = self.broadcast_recv_socket.recvfrom(1024)
                print(len(message), addr)
                if message is not None:
                    # a valid message was received
                    uuid, opcode, flags, striplen = struct.unpack("!16sIII", message[:header_len])
                    # check if the light device already exists
                    # create database type object
                    new_light = Light()
                    new_light.address = addr[0]
                    new_light.port = addr[1]
                    new_light.uuid = uuid.decode("utf-8")
                    new_light.length = striplen
                    self.available_light_tracker.add_available_light(new_light)
            except socket.timeout:
                continue
