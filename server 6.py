import socket
import struct

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.1.100', 5000))  # Replace with your server's IP and the correct port

while True:
    data = s.recv(8)  # Expecting 8 bytes, 4 for the float and 4 for the integer
    if data:
        distance, identifier = struct.unpack('fi', data)
        if identifier == 1:
            print(f"Distance from lidar3: {distance} cm")
        elif identifier == 2:
            print(f"Distance from lidar2: {distance} cm")
    else:
        break

s.close()