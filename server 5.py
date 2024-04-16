import socket
import struct
import win32api

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.106.25", 5000))

screen_width = win32api.GetSystemMetrics(0)
screen_height = win32api.GetSystemMetrics(1)
win32api.SetCursorPos((screen_width // 2, screen_height // 2))

cm_per_screen_width = screen_width / 25
cm_per_screen_height = screen_height / 25

while True:
    data = s.recv(8)  # Receive 8 bytes now, for float and int
    if data:
        distance_from_origin, identifier = struct.unpack('fi', data)  # Unpack as float and int
        print(distance_from_origin, identifier)

        if identifier == 1:  # Data from lidar3 for X movement
            mapped_x_position = int(distance_from_origin * cm_per_screen_width)
            current_y = win32api.GetCursorPos()[1]
            win32api.SetCursorPos((mapped_x_position, current_y))
            
        elif identifier == 2:  # Data from lidar2 for Y movement
            current_x = win32api.GetCursorPos()[0]
            mapped_y_position = int(distance_from_origin * cm_per_screen_height)
            win32api.SetCursorPos((current_x, mapped_y_position))
            
    else:
        break

s.close()
