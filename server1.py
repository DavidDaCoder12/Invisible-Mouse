# server.py modifications
'''
sudo python3 server1.py
'''

import socket
import time
from threading import Thread
import lidar3

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 5000))
s.listen(5)
print('Server is now running')

def handle_client(clientsocket):
    def send_lidar_data(current, previous):
        distance_diff = current - previous
        direction = "didn't move"
        if previous > current:
            direction = "moved closer"
        elif previous < current:
            direction = "moved away"

        message = f"Current Distance: {current}cm, Difference: {distance_diff}cm - {direction}\n"
        clientsocket.send(message.encode('utf-8'))

    # Run lidar1.main() in a separate thread to avoid blocking
    lidar_thread = Thread(target=lidar3.main, args=(send_lidar_data,))
    lidar_thread.start()

while True:
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established.")
    Thread(target=handle_client, args=(clientsocket,)).start()
