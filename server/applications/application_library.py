import importlib.util
import sys
from server.applications.firelight_application import FirelightApplicationFactory

class ApplicationLibrary(object):

    def __init__(self):
        self.applications = {
            "firelight_mp4": FirelightApplicationFactory("/mnt/c/Users/gfvan/Downloads/firelight.mp4")
        }
    
    def get_application(self, application_id: str):
        return self.applications.get(application_id)
