from threading import Thread, Timer
import socket
from server.device.registry import DeviceRegistry
from server.model.light import LightDevice, NeoPixel, GridSpace
from server.device.udpcommunicator import UDPCommunicator
from server.device.statemanager import StateManager
import struct

class UDPFinder(object):

    def __init__(self, device_registry: DeviceRegistry):
        self.listening_socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.listening_socket.settimeout(1)
        self.listening_socket.bind(("", 2650))
        self.timer_running = False
        self.timer: Timer = None

        self.registry = device_registry

    def start_timeout(self):
        self.timer_running = True
        self.timer = Timer(5, self.end_timeout)
        self.timer.start()
        #print("Timer started")

    def end_timeout(self):
        self.timer_running = False
        #print("Timer stopped")

    def run_find_thread(self):
        if self.timer is not None and self.timer.is_alive():
            self.timer.cancel()
        
        self.start_timeout()
        while self.timer_running:
            try:
                data, addr = self.listening_socket.recvfrom(1024)
                self.parse_identifier_message(data, addr)
            except socket.timeout:
                continue
    
    def parse_identifier_message(self, data, address):
        """
        light_id: int (4), num_lights: int (4), token string 16, light_grid str * 
        """
        static_portion = data[:6+1+16+4]
        light_grid_string = data[23:]
        print(light_grid_string)
        light_grid_string = light_grid_string.decode('utf-8')
        light_id, data_port, num_lights, token_str = struct.unpack("!6sIB16s", static_portion)
        # convert 6 byte mac to string
        light_id = "{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}".format(
            light_id[0],
            light_id[1],
            light_id[2],
            light_id[3],
            light_id[4],
            light_id[5]
        )
        light_grid, neopixel_list = self.parse_grid_string(light_grid_string)

        if self.registry.check_device_exists(light_id):
            light_object = self.registry.get_light_device(light_id)
        else:
            # create a new light device
            print(light_id, num_lights, token_str)
            new_state_manager = StateManager(light_grid_string)
            new_communicator = UDPCommunicator(new_state_manager, (address[0], data_port))
            new_device = LightDevice(light_id,
                                     num_lights,
                                     255,
                                     light_grid,
                                     neopixel_list,
                                     new_state_manager,
                                     new_communicator,
                                     True)
            self.registry.add_light_device(new_device)
            new_communicator.start()

    @staticmethod
    def parse_grid_string(grid_string: str):
        lines = grid_string.splitlines()
        end_result = []
        neopixel_dict = {}
        for line in lines:
            values = line.split(" ")
            row = []
            for value in values:
                if value != ".":
                    index = int(value)
                    new_grid_space = NeoPixel(index, 0, 0, 0)
                    neopixel_dict[index] = NeoPixel
                else:
                    new_grid_space = GridSpace()
                row.append(new_grid_space)
            end_result.append(row)
        return end_result, neopixel_dict