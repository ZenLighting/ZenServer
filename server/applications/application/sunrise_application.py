import pydantic
from server.applications.application.light_application import LightApplicationTemplate
from server.applications.builders.basebuilder import LightApplicationBuilder
from server.model.grid import LightGrid
import time
import datetime

class SunriseApplicationArg(pydantic.BaseModel):
    duration_in_seconds: int
    blink_after: bool = False

class BlinkStateInformation(object):
    last_time: datetime.datetime
    on: bool

class SunriseApplication(LightApplicationTemplate):

    def __init__(self, grid_object: LightGrid, args: SunriseApplicationArg):
        LightApplicationTemplate.__init__(self, grid_object)
        self.args = args
        self.time_passed = 0
        self.end_color = [255, 255, 20]
        self.frame_multiplier = self.args.duration_in_seconds*30 # THIS IS HOW MANY FRAMES we should be lighting up on
        self.color_iterative = [
            self.end_color[0]/self.frame_multiplier,
            self.end_color[1]/self.frame_multiplier,
            self.end_color[2]/self.frame_multiplier
        ]
        self.actual_color = [0, 0, 0]
        self.state = "START"

        self.blink_state_information = BlinkStateInformation()
        self.blink_state_information.last_time = None
    
    def state_start(self):
        self.grid.set_grid_color(0, 0, 0)
        self.state = "SUNRISE"

    def state_sunrise(self):
        self.actual_color[0] += self.color_iterative[0]
        self.actual_color[1] += self.color_iterative[1]
        self.actual_color[2] += self.color_iterative[2]
        self.grid.set_grid_color(int(self.actual_color[0]), int(self.actual_color[1]), int(self.actual_color[2]))
        
        if [int(self.actual_color[0]), int(self.actual_color[1]), int(self.actual_color[2])] == self.end_color:
            self.state = "BLINK"
            if self.args.blink_after is False:
                self.stop()
                return
    
    def state_blink(self):
        if self.blink_state_information.last_time is None or datetime.datetime.now() - self.blink_state_information.last_time > datetime.timedelta(seconds=10):
            self.blink_state_information.last_time = datetime.datetime.now()
            self.blink_state_information.on = not self.blink_state_information.on

            if self.blink_state_information.on:
                self.grid.set_grid_color(255, 255, 255)
            else:
                self.grid.set_grid_color(0, 0, 0)


        
    def tick(self):
        print("Ticking")
        print("SUNRISE", self._stop, self._pause)
        if self.state == "START":
            print("START")
            self.state_start()
        elif self.state == "SUNRISE":
            print("SUNRISE")
            self.state_sunrise()
        elif self.state == "BLINK":
            print("BLINK")
            self.state_blink()
        time.sleep(1/30)
        print("SUNRISE", self._stop, self._pause)

class SunriseApplicationFactory(LightApplicationBuilder):
    def __call__(self, grid_object: LightGrid, args) -> SunriseApplication:
        app_args = SunriseApplicationArg.parse_obj(args)
        new_sunrise_application = SunriseApplication(grid_object, app_args)
        return new_sunrise_application