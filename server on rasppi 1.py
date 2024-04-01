import socket
import time
from threading import Timer
import lidar1

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 5000))
s.listen(5)
print('Server is now running')

def background_controller(clientsocket):
    message = 'Lidar data'
    clientsocket.send(bytes(message, "utf-8"))

    for i in range(10):
        lidar1.read_data()

    Timer(5, background_controller, [clientsocket]).start()

while True:
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established.")
    background_controller(clientsocket)

