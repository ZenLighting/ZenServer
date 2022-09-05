import time
from server.applications.application.light_application import LightApplicationTemplate
from server.applications.builders.basebuilder import LightApplicationBuilder
from server.model.grid import LightGrid
import cv2
import numpy as np
import pydantic

class FirelightApplicationFromVideo(LightApplicationTemplate):

    def __init__(self, firelight_mp4, grid_object: LightGrid):
        LightApplicationTemplate.__init__(self, grid_object)
        self.firelight_mp4 = firelight_mp4
        self.fire_video: cv2.VideoCapture = cv2.VideoCapture(self.firelight_mp4)

    def tick(self):
        print("HERE")
        ret, frame = self.fire_video.read()
        frame: np.ndarray
        frame = cv2.resize(frame, [self.grid.grid_x, self.grid.grid_y])
        for y, row in enumerate(frame):
            for x, col in enumerate(row):
                self.grid.set_index_color(y, x, col[0], col[1], col[2])
        time.sleep(1/30)
        if not self.fire_video.isOpened():
            self.fire_video = cv2.VideoCapture(self.firelight_mp4)
        #cv2.imshow("frame", frame)

class FirelightApplicationFactory(LightApplicationBuilder):

    def __init__(self, fire_mp4_path: str):
        self.fire_mp4_path = fire_mp4_path

    def __call__(self, grid_object: LightGrid, args) -> FirelightApplicationFromVideo:
        new_firelight_application = FirelightApplicationFromVideo(self.fire_mp4_path, grid_object)
        return new_firelight_application

if __name__ == "__main__":
    Factory = FirelightApplicationFactory("/mnt/c/Users/gfvan/Downloads/firelight.mp4")
    proc = Factory(None)
    proc.start()
    while True:
        time.sleep(1)
