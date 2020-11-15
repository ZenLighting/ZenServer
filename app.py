"""from server.finders.udpfinder import UDPFinder
from server.device.registry import DeviceRegistry
from server.model.light import LightDevice
from server.device.udpcommunicator import UDPCommunicator
from server.device.statemanager import StateManager
from threading import Thread
device_registry = DeviceRegistry()
finder = UDPFinder(device_registry)

light = None

def run_fin():
    while True:
        finder.run_find_thread()
Thread(target=run_fin).start()

while True:
    inp = input("input a to find, b to send all white, c to clear")
    if inp == "b":
        light: LightDevice = device_registry.get_light_device("48:3f:da:0d:c2:9f")
        state: StateManager = light.state
        state.set_row(0, 255, 255, 255)
        print(state.get_state())
    elif inp == "c":
        light: LightDevice = device_registry.get_light_device("48:3f:da:0d:c2:9f")
        state: StateManager = light.state
        state.set_row(0, 0, 0, 0)
        print(state.get_state())
    else:
        print("Try Again")
"""
from server import App

App()