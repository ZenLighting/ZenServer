from server.finders.udpfinder import UDPFinder
from server.device.registry import DeviceRegistry
from server.model.grid import NeoPixel
from server.rooms.room import Room
from server.model.light import LightDevice
import time
from threading import Thread

r = DeviceRegistry()
u = UDPFinder(r)

def infinite_find():
    while True:
        u.run_find_thread()

Thread(target=infinite_find).start()

print("Awaiting signal from both lights")
while(len(r.list_registered_macs()) < 2):
    time.sleep(1)

print("Have lights", r.list_registered_macs())
print("Creating room")
macs_list_len_2 = r.list_registered_macs()
light_1: LightDevice = r.get_light_device("48:3f:da:0d:c2:9f") # circle
light_2: LightDevice = r.get_light_device("48:3f:da:0d:c7:e8") # line

room = Room("bedroom")
# for now just add one light @[1,1]
room.add_light(light_1, 1, 1)
print(id(room.grid[8][1]), id(light_1.state.grid[7][0]))
print()
room.add_light(light_2, 0, 0)
print(id(room.grid[0][0]), id(light_1.state.grid[0][0]))

for row in room.grid:
    print(row)

print(len(room.grid))

light_1.state.set_all(255, 255, 255)
while(True):
    print("setting white")
    room.set_all(255, 0, 0)
    #light_2.state.set_all(255, 255, 255)
    time.sleep(5)
    print("Setting Black")
    #print(room.grid[0][0])
    #print(light_2.state.light_dict[0])
    #light_2.state.set_all(0,0,0)
    room.set_all(0, 0, 0)
    time.sleep(5)

    """for row in room.grid:
        for light in row:
            if isinstance(light, NeoPixel):
                light: NeoPixel
                light.r = 0
                light.g = 0
                light.b = 0"""
    #for row in room.grid:
    #    print(row)"""