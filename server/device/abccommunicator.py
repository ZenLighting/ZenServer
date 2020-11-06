from threading import Thread
from abc import ABC, abstractmethod
import time

class ABCCommunicator(Thread, ABC):

    def __init__(self, state_manager):
        Thread.__init__(self)
        self.running = True
        self.state_manager = state_manager

    def run(self):
        while self.running:
            time.sleep(1/30)
            brightness, state = self.state_manager.get_state()
            self.send_frame(brightness, state)

    @abstractmethod
    def send_frame(self, brightness: int, state: list):
        pass