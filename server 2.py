import socket
import struct  # Import struct to handle binary data (integers)
import win32api

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.34.25", 5000))

while True:
    # Receive 4 bytes from the server, since an integer is 4 bytes
    data = s.recv(4)
    # Check if data is not empty
    if data:
        # Unpack the received bytes as a signed integer ('i')
        distance_from_origin = struct.unpack('i', data)[0]
        print(distance_from_origin)
        win32api.SetCursorPos((540,distance_from_origin))
        # Example usage with win32api.SetCursorPos, uncomment and adjust as needed
        # win32api.SetCursorPos((540, distance_from_origin))
    else:
        # If no data is received, break the loop to avoid an infinite loop
        break