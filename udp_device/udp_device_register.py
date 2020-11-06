import socket

class UdpDeviceRegister(object):
    
    def __init__(self, udp_registery: ):
        self.bcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.bcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.bcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.bcast_socket.bind(("", 76808))
        self.running = True

    def listen(self):
        while self.running:
            (data, addr) = self.bcast_socket.recvfrom(1024)
