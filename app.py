from server.finders.udpfinder import UDPFinder
from server.device.registry import DeviceRegistry

device_registry = DeviceRegistry()
finder = UDPFinder(device_registry)

while True:
    finder.run_find_thread()
"""from server import App

App(mqtt_host="mosquitto")"""