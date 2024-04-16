import socket
import time
from threading import Thread
import struct
import lidar3
import lidar2

origin1 = None
origin2 = None

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 5000))
s.listen(5)
print('Server is now running')

def handle_client(clientsocket):
    def send_lidar_data1(current, _):
        global origin1
        if origin1 is None:
            origin1 = current
        distance_from_origin = current - origin1
        # Send distance along with an identifier '1' for lidar3
        message = struct.pack('fi', distance_from_origin, 1)  # 'f' for float, 'i' for int identifier
        clientsocket.send(message)

    def send_lidar_data2(current, _):
        global origin2
        if origin2 is None:
            origin2 = current
        distance_from_origin = current - origin2
        # Send distance along with an identifier '2' for lidar2
        message = struct.pack('fi', distance_from_origin, 2)  # 'f' for float, 'i' for int identifier
        clientsocket.send(message)

    Thread(target=lidar3.main, args=(send_lidar_data1,)).start()
    Thread(target=lidar2.main, args=(send_lidar_data2,)).start()

while True:
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established.")
    Thread(target=handle_client, args=(clientsocket,)).start()
