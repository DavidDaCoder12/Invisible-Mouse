import socket
import struct
from threading import Thread, Lock
import lidar3
import lidar2

class LidarServer:
    def __init__(self, port=5000):
        self.origin1 = None
        self.origin2 = None
        self.lock = Lock()
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('', port))
        self.server_socket.listen(5)
        print('Server is now running on port', port)

    def run(self):
        try:
            while True:
                clientsocket, address = self.server_socket.accept()
                print(f"Connection from {address} has been established.")
                Thread(target=self.handle_client, args=(clientsocket,)).start()
        except Exception as e:
            print("Server error:", e)
        finally:
            self.server_socket.close()

    def handle_client(self, clientsocket):
        try:
            Thread(target=lidar3.main, args=(self.send_lidar_data1_wrapper(clientsocket),)).start()
            Thread(target=lidar2.main, args=(self.send_lidar_data2_wrapper(clientsocket),)).start()
        except Exception as e:
            print("Error handling client:", e)
        finally:
            clientsocket.close()

    def send_lidar_data1_wrapper(self, clientsocket):
        def send_lidar_data1(current, _):
            with self.lock:
                if self.origin1 is None:
                    self.origin1 = current
                distance_from_origin = current - self.origin1
            message = struct.pack('fi', distance_from_origin, 1)
            clientsocket.send(message)
        return send_lidar_data1

    def send_lidar_data2_wrapper(self, clientsocket):
        def send_lidar_data2(current, _):
            with self.lock:
                if self.origin2 is None:
                    self.origin2 = current
                distance_from_origin = current - self.origin2
            message = struct.pack('fi', distance_from_origin, 2)
            clientsocket.send(message)
        return send_lidar_data2

if __name__ == '__main__':
    server = LidarServer()
    server.run()
