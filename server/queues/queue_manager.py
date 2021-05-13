from queue import Queue

class InputQueueManager(object):

    def __init__(self):
        self.queues_by_name = {}

    def get_queue(self, name: str) -> Queue:
        if self.queues_by_name.get(name) is None:
            self.queues_by_name[name] = Queue()
        return self.queues_by_name[name]