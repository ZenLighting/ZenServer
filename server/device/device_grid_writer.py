from server.design_patterns.observable import Observer
from server.model.sqlite_models import LightDeviceModel
from server.model.grid import LightGrid
from server.model.grid import LightGridEvents
import socket
from queue import Empty, Queue
import time
import struct

import threading

class DeviceGridWriter(object):

    def __init__(self, device_model: LightDeviceModel, device_grid: LightGrid, communicator_socket: socket.socket=None):
        self.model = device_model
        self.grid = device_grid
        self.message_queue = Queue(maxsize=5)

        if communicator_socket is None:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
            self.socket.bind(("", 0))
        else:
            self.socket = communicator_socket

        self.grid_consumer_30_fps = threading.Thread(target=self.grid_state_message_consumer)
        self.grid_consumer_30_fps.start()

        super_self = self
        class DeviceGridStateChange(Observer):
            def trigger(self, event, observable):
                #print(event, observable)
                super_self.add_change_to_queue()

        myObserver = DeviceGridStateChange()
        self.grid.attach(LightGridEvents.GRID_CHANGE, myObserver)
    
    def add_change_to_queue(self):
        message_bytes = struct.pack("!BB", 0, 0)
        for pixel in self.grid.pixels_by_index:
            message_bytes+=struct.pack("!BBB", pixel.g, pixel.r, pixel.b)
        
        if self.message_queue.full():
            self.message_queue.get() # pop off front
            self.message_queue.put(message_bytes) # add new message to back of queue
        else:
            self.message_queue.put(message_bytes)

    def grid_state_message_consumer(self):
        while True:
            try:
                message = self.message_queue.get(timeout=1)
                if self.model.last_address is not None:
                    #print("sent to light", message)
                    self.socket.sendto(message, (self.model.last_address, 1261))
                time.sleep(1/30)
            except Empty:
                continue

