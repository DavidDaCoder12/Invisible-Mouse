# server.py modifications
'''
sudo python3 server1.py
'''

import socket
import time
from threading import Thread
import struct
import lidar3

origin = None

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 5000))
s.listen(5)
print('Server is now running')

def handle_client(clientsocket):
    def send_lidar_data(current, _):
        global origin

        # If the origin hasn't been set, use the current distance as the origin
        if origin is None:
            origin = current

        # Calculate the distance from the current position to the origin
        distance_from_origin = current - origin

        # You can include logic for direction based on how you want to interpret movement
        '''direction = "at the origin"
        if distance_from_origin > 0:
            direction = "moved away from the origin"
        elif distance_from_origin < 0:
            direction = "moved closer to the origin"'''

        # Prepare and send the message
        message = struct.pack('i', distance_from_origin)
        clientsocket.send(message)

    # Run lidar1.main() in a separate thread to avoid blocking
    lidar_thread = Thread(target=lidar3.main, args=(send_lidar_data,))
    lidar_thread.start()

while True:
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established.")
    Thread(target=handle_client, args=(clientsocket,)).start()
