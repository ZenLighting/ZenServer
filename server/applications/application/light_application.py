import enum
from queue import Empty
from typing import Any
from server.model.grid import LightGrid
from server.model.light import LightDeviceModel
from multiprocessing import Queue, Process
from threading import Thread
from typing import Dict
import time
from server.design_patterns.observable import RevisedObservable

class LightApplicationEvents(enum.Enum):
    FINISHED="finished"

class LightApplicationTemplate(Thread, RevisedObservable):

    def __init__(self, light_grid: LightGrid):
        Thread.__init__(self)
        RevisedObservable.__init__(self)
        self.grid = light_grid
        self.input_message_queue = Queue(5) # this is where any messages can be passed between programs
        self._message_consumer = Thread(target=self._consume_message_queue)
        self._message_consumer.start()
        self._stop = False
        self._pause = False
    
    def _consume_message_queue(self):
        while True:
            try:
                input_message = self.input_message_queue.get(timeout=1)
                self.handle_input_message(input_message)
            except Empty:
                continue

    def run(self):
        while not self._stop:
            if self._pause:
                time.sleep(1)
                continue
            else:
                self.tick()
        self.clean()
        self.emit(LightApplicationEvents.FINISHED, None)            

    def pause(self):
        self._pause = True
    
    def resume(self):
        self._pause = False
    
    def stop(self):
        self._stop = True
    
    def handle_input_message(self, input_message: Any):
        raise(NotImplementedError())

    def tick(self):
        pass

    def clean(self):
        pass

