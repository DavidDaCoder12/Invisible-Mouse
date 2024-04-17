import socket
from threading import Thread, Lock, Event
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

def send_combined_data(clientsocket):
    # Function to send data when both lidar readings are updated
    while True:
        update_event.wait()  # Wait for both distances to be updated
        with lock:
            message = f"{current_distances['lidar1']:.2f}, {current_distances['lidar2']:.2f}\n"
            clientsocket.send(message.encode())
            print(f"Sent: {message.strip()}")  # Log what was sent
            update_event.clear()  # Reset the event until next update

def update_lidar_data(lidar_key, current):
    """Update lidar data in a thread-safe manner and trigger sending when ready."""
    global origin1, origin2
    with lock:
        origin = origin1 if lidar_key == 'lidar1' else origin2
        if origin is None:
            if lidar_key == 'lidar1':
                origin1 = current
            elif lidar_key == 'lidar2':
                origin2 = current
            origin = current
        distance_from_origin = current - origin
        current_distances[lidar_key] = distance_from_origin

        # Check if both distances are updated
        if current_distances['lidar1'] is not None and current_distances['lidar2'] is not None:
            update_event.set()  # Signal that both data points are ready

def handle_client(clientsocket):
    """Handle each client connection in a dedicated thread."""
    print(f"Connection from {clientsocket.getpeername()} has been established.")
    
    # Start the thread to send combined data
    sender_thread = Thread(target=send_combined_data, args=(clientsocket,))
    sender_thread.start()

    # Start threads for each lidar
    lidar1_thread = Thread(target=lidar3.main, args=(lambda current, _: update_lidar_data('lidar1', current),))
    lidar2_thread = Thread(target=lidar2.main, args=(lambda current, _: update_lidar_data('lidar2', current),))

    lidar1_thread.start()
    lidar2_thread.start()

    lidar1_thread.join()
    lidar2_thread.join()
    sender_thread.join()

while True:
    clientsocket, _ = s.accept()
    Thread(target=handle_client, args=(clientsocket,)).start()
