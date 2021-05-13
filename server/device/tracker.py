from queue import Empty
from threading import Thread
from server.queues.queue_manager import InputQueueManager
import time
from server.types.messages.device_registration import DeviceRegistrationMessage
import logging

log = logging.getLogger(__name__)

class DeviceTracker(Thread):

    def __init__(self, queue_manager: InputQueueManager):
        Thread.__init__(self)
        self.consumption_queue = queue_manager.get_queue("registration")
        self.devices_recieved = {}

    def run(self):
        while True:
            try:
                item = self.consumption_queue.get(timeout=1)
                # a registration message was recieved
                cur_time = time.time()
                message_data = DeviceRegistrationMessage(**item)
                message_data.last_detected = cur_time
                self.devices_recieved[message_data.dId] = message_data.dict()
                #log.debug(f"Got registry for {message_data.dict()}")
            except Empty:
                continue