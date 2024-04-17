import socket
import time
from threading import Thread, Lock, Event
import struct
import lidar3
import lidar2

origin1 = None
origin2 = None
current_distances = {'lidar1': None, 'lidar2': None}
update_event = Event()
lock = Lock()  # A lock for thread-safe operations on origins

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 5000))
s.listen(5)
print('Server is now running')

def handle_client(clientsocket):
    global origin1, origin2, current_distances

    def send_combined_data():
        while True:
            update_event.wait()  # Wait for both distances to be updated
            with lock:
                message = f"{current_distances['lidar1']:.2f}, {current_distances['lidar2']:.2f}\n"
                clientsocket.send(message.encode())
                update_event.clear()  # Reset the event until next update

    def update_lidar_data(lidar_key, current):
        nonlocal origin1, origin2
        with lock:
            origin = origin1 if lidar_key == 'lidar1' else origin2
            if origin is None:
                if lidar_key == 'lidar1':
                    origin1 = current
                else:
                    origin2 = current
                origin = current
            distance_from_origin = current - origin
            current_distances[lidar_key] = distance_from_origin
            # Check if both distances are updated
            if current_distances['lidar1'] is not None and current_distances['lidar2'] is not None:
                update_event.set()  # Signal that both data points are ready

    Thread(target=send_combined_data).start()
    Thread(target=lidar3.main, args=(lambda current, _: update_lidar_data('lidar1', current),)).start()
    Thread(target=lidar2.main, args=(lambda current, _: update_lidar_data('lidar2', current),)).start()

while True:
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established.")
    Thread(target=handle_client, args=(clientsocket,)).start()
