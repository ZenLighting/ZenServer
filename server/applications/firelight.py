from random import randint
import time
from typing import Tuple
import requests

COLORS = [(255, 0, 0), (255, 50,0), (255,100,0)]

class FireLightApplication(object):

    def __init__(self, light_id, server="http://192.168.1.11:8080"):
        self.light_id = light_id
        self.server = server

        # get light information
        device_response = requests.get(f"{self.server}/device/{self.light_id}")
        
        # get grid from device_response
        self.current_color = (0, 0, 0)
        self.frames_amt = 10


    def run(self):
        last_a = 0
        while True:
            # choose random color from red, orange, and yellow
            """a = randint(0, 2)
            while last_a == a:
                a = randint(0, 2)
            last_a = a

            next_color = COLORS[a]"""
            frames_amt = randint(5, 30)
            generated_frames = self.color_fade_frames(
                self.current_color,
                (randint(50, 255), randint(0, 50), 0), 
                frames_amt)

            for i in generated_frames:
                response = requests.post(f"{self.server}/device/{self.light_id}/set_color", json={
                    "color-protocol": "rgb",
                    "r": i[0],
                    "g": i[1],
                    "b": i[2]
                })
                print(i[0], i[1], i[2])
                print(response.text)
                time.sleep(1/30)
            self.current_color = (i[0], i[1], i[2])
            time.sleep(1/30)
    
    @staticmethod
    def color_fade_frames(
        color_1: Tuple[int, int, int],
        color_2: Tuple[int, int, int],
        frames: int):

        r_rate_of_change = (color_2[0] - color_1[0])/frames
        g_rate_of_change = (color_2[1] - color_1[1])/frames
        b_rate_of_change = (color_2[2] - color_1[2])/frames

        new_frames = []
        for i in range(frames):
            new_color = (
                min(color_1[0] + int(r_rate_of_change*i), 255),
                min(color_1[1] + int(g_rate_of_change*i), 255),
                min(color_1[2] + int(b_rate_of_change*i), 255)
            )
            new_frames.append(new_color)
        return new_frames

f = FireLightApplication(2)
f.run()