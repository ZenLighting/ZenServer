import socket
import time
import json
from threading import Thread

fd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
fd.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
fd.bind(("", 1261))


def broadcast_thread():
    while True:
        fd.sendto(json.dumps({
            "name": "test-grid-light",
            "strip": {
                "length": 3
            },
            "communication": {
                "protocols": [0, 1, 2]
            }
        }).encode("utf-8"),
        ("localhost",1260))
        time.sleep(1)

def recv_thread():
    while True:
        data, addr = fd.recvfrom(1024)
        print(data, addr)

Thread(target=broadcast_thread).start()
Thread(target=recv_thread).start()