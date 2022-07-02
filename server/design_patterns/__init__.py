from typing import Any
from typing import List

class Observer(object):
    def trigger(self, event: Any, observable: Any):
        pass

class Observable(object):

    def __init__(self):
        self.observers = {}

    def attach(self, event: Any, observer: Observer):
        event_array = self.observers.get(event)
        if event_array is None:
            self.observers[event] = []
            event_array = self.observers.get(event)
        event_array: List
        event_array.append(observer)
    
    def trigger_event(self, event: Any):
        if self.observers.get(event):
            for observer in self.observers.get(event):
                observer.trigger(event, self)
        else:
            print("Observable tried to trigger event with no observers")
