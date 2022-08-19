from server.applications.application_library import ApplicationLibrary
from server.applications.light_application import LightApplicationEvents, LightApplicationTemplate
from server.model.grid import LightGrid
from server.design_patterns.observable import Observer, RevisedObserver
from typing import Dict

class LightApplicationManager(RevisedObserver):

    def __init__(self, application_library: ApplicationLibrary):
        self.library = application_library
        self._running_applications: Dict[int, LightApplicationTemplate] = {}
    
    def trigger(self, observable, event, data):
        if event == LightApplicationEvents.FINISHED:
            self._running_applications.pop(id(observable))
    
    def start_application(self, application_name, light_grid: LightGrid):
        application_factory = self.library.get_application(application_name)
        if application_factory is not None:
            new_application = application_factory(light_grid)
            self._running_applications[id(new_application)] = new_application
            new_application.attach(self)
            new_application.start()
            return new_application
        return None
        
    def pause_application(self, application_id: int):
        application = self._running_applications.get(application_id)
        if application is not None:
            application.pause()
    
    def resume_application(self, application_id: int):
        application = self._running_applications.get(application_id)
        if application is not None:
            application.resume()
    
    def kill_application(self, application_id):
        application = self._running_applications.get(application_id)
        if application is not None:
            application.stop()
    

