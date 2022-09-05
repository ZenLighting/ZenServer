import importlib.util
import sys
from server.applications.application.firelight_application import FirelightApplicationFactory
from server.applications.application.sunrise_application import SunriseApplicationBuilder

class ApplicationLibrary(object):

    def __init__(self):
        # look in /opt/zenlight/applications for individual application libraries

        self.applications = {
            "firelight_mp4": FirelightApplicationFactory("/mnt/c/Users/gfvan/Downloads/firelight.mp4"),
            "sunrise": SunriseApplicationBuilder()
        }
    
    def get_application(self, application_id: str):
        return self.applications.get(application_id)
