import socket
import struct  # Import struct to handle binary data (integers)
import win32api

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("10.255.139.107", 5000))

screen_width = win32api.GetSystemMetrics(0)
screen_height = win32api.GetSystemMetrics(1)

# Set the cursor to the center of the screen initially
win32api.SetCursorPos((screen_width // 2, screen_height // 2))

# Adjust this value if 'distance_from_origin' is not in centimeters
cm_per_screen_width = screen_width / 25 

while True:
    # Receive 4 bytes from the server, since an integer is 4 bytes
    data = s.recv(4)
    # Check if data is not empty
    if data:
        # Unpack the received bytes as a signed float ('f')
        distance_from_origin = struct.unpack('f', data)[0]
        print(distance_from_origin)

        # Calculate the cursor's x position based on the received distance
        mapped_x_position = int(distance_from_origin * cm_per_screen_width)
        win32api.SetCursorPos((mapped_x_position, 540))
    else:
        # If no data is received, break the loop to avoid an infinite loop
        break

s.close()
