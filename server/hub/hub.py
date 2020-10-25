from server.mqtt.mqtt_service import MqttService
from server.model.light import LightDevice
import json
import struct
import base64

class LightMQTTConnection(object):

    def __init__(self, mqtt_client: MqttService, light_data: LightDevice):
        self.data: LightDevice = light_data
        self.mqtt = mqtt_client
    
    def send_color(self, r, g, b, brightness):
        # make the bytes stream
        brightness_uchar = struct.pack("BB", brightness, self.data.num_leds)
        rgb_struct = struct.pack("BBB", r, g, b)
        byte_string = brightness_uchar
        for i in range(self.data.num_leds):
            byte_string += rgb_struct
        # 
        self.mqtt.publish(f"zen/{self.data.light_id}/set", byte_string)