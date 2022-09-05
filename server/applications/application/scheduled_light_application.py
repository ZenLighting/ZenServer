from datetime import datetime
import time
from server.applications.application.light_application import LightApplicationTemplate
from server.design_patterns.observable import Observer

class ScheduledLightApplicationWrapper(LightApplicationTemplate, Observer):

    def __init__(self, time_to_run: datetime, application_to_wrap: LightApplicationTemplate):
        self._await_until_time = time_to_run
        self._time_trigger_met = False
        self.application_to_wrap = application_to_wrap
        self.application_to_wrap.attach(self)
    
    def trigger(self, observable, event, data):
        self.emit(event, data)
    
    def tick(self):
        # check if datetime is correct
        if self._time_trigger_met:
            self.application_to_wrap.tick()
            self._stop = self.application_to_wrap.stop()
        else:
            current_time = datetime.now()
            if current_time > self._await_until_time:
                self._time_trigger_met = True
            else:
                time.sleep(1)

