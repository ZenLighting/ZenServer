import requests
import time
import json

for i in range(360):
    print("HUE", i)
    requests.post(
        "http://localhost:5000/device/Test1/set_static",
        json={
            "color_scheme": "hsv",
            "value": [i/360, 1, 1]
        }
    )
    time.sleep(1/60)
