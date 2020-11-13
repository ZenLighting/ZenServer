import socket

multicast_group = ('', 2650)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.bind(multicast_group)

while(True):
    msg, addr = sock.recvfrom(1024)
    print(msg, addr)