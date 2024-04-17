import socket
import time
from threading import Thread, Lock
import struct
import lidar3
import lidar2

origin1 = None
origin2 = None
lock = Lock()  # A lock for thread-safe operations on origins

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 5000))
s.listen(5)
print('Server is now running')

def handle_client(clientsocket):
    global origin1, origin2
    
    def send_lidar_data1(current, _):
        nonlocal origin1
        with lock:
            if origin1 is None:
                origin1 = current
            distance_from_origin = current - origin1
        message = struct.pack('fi', distance_from_origin, 1)
        clientsocket.send(message)

    def send_lidar_data2(current, _):
        nonlocal origin2
        with lock:
            if origin2 is None:
                origin2 = current
            distance_from_origin = current - origin2
        message = struct.pack('fi', distance_from_origin, 2)
        clientsocket.send(message)

    Thread(target=lidar3.main, args=(send_lidar_data1,)).start()
    Thread(target=lidar2.main, args=(send_lidar_data2,)).start()

while True:
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established.")
    Thread(target=handle_client, args=(clientsocket,)).start()
