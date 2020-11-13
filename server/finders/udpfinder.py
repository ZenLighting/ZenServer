from threading import Thread, Timer
import socket
from server.device.registry import DeviceRegistry
from server.model.light import LightDevice
import struct

class UDPFinder(object):

    def __init__(self, device_registry: DeviceRegistry):
        self.listening_socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.listening_socket.bind(("", 2650))
        self.timer_running = False
        self.timer: Timer = None

        self.registry = device_registry

    def start_timeout(self):
        self.timer_running = True
        self.timer = Timer(5, self.end_timeout)
        self.timer.start()
        print("Timer started")

    def end_timeout(self):
        self.timer_running = False
        print("Timer stopped")

    def run_find_thread(self):
        if self.timer is not None and self.timer.is_alive():
            self.timer.cancel()
        
        self.start_timeout()
        while self.timer_running:
            data, addr = self.listening_socket.recvfrom(1024)
            self.parse_identifier_message(data)
    
    def parse_identifier_message(self, data):
        """
        light_id: int (4), num_lights: int (4), token string 16, light_grid str * 
        """
        static_portion = data[:6+1+16]
        light_grid_string = data[4+4+16:]
        light_id, num_lights, token_str = struct.unpack("!6sB16s", static_portion)
        print("{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}".format(light_id[0],light_id[1],light_id[2],light_id[3],light_id[4],light_id[5]))
        if self.registry.check_device_exists(light_id):
            light_object = self.registry.get_light_device(light_id)
        else:
            # create a new light device
            print(light_id, num_lights, token_str)
            #new_device = LightDevice()
            