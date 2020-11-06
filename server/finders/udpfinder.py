from threading import Thread, Timer
import socket
from server.device.registry import DeviceRegistry
import struct

class UDPFinder(object):

    def __init__(self, device_registry: DeviceRegistry):
        self.listening_socket = socket.socket(socket.SOL_SOCKET, socket.SOCK_DGRAM)
        self.listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listening_socket.bind(("", 2560))
        self.timer_running = False
        self.timer: Timer = None

        self.registry = device_registry

    def start_timeout(self):
        self.timer_running = True
        self.timer = Timer(5, self.end_timeout)
        self.timer.start()

    def end_timeout(self):
        self.timer_running = False

    def run_find_thread(self):
        if self.timer is not None or self.timer.is_alive():
            self.timer.cancel()
        self.start_timeout()
        while self.timer_running:
            data, addr = self.listening_socket.recv(1024)
    
    def parse_identifier_message(self, data):
        """
        light_id: int (4), num_lights: int (4), token string 16, light_grid str * 
        """
        static_portion = data[:4+4+16]
        light_grid_string = data[4+4+16:]
        light_id, num_lights, token_str = struct.unpack("!IIs16", static_portion)
        
        if self.registry.check_device_exists(light_id):
            light_object = self.registry.get_light_device(light_id)
            