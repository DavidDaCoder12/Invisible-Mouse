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

alpha = 0.3  # Smoothing factor for EMA
prev_x = screen_width // 2
prev_y = screen_height // 2

while True:
    data = s.recv(8)
    if data:
        distance_from_origin, identifier = struct.unpack('fi', data)
        print(distance_from_origin, identifier)

        if identifier == 1:
            target_x = int(distance_from_origin * cm_per_screen_width)
            smoothed_x = int(alpha * target_x + (1 - alpha) * prev_x)
            prev_x = smoothed_x
            current_y = win32api.GetCursorPos()[1]
            win32api.SetCursorPos((smoothed_x, current_y))

        elif identifier == 2:
            target_y = int(distance_from_origin * cm_per_screen_height)
            smoothed_y = int(alpha * target_y + (1 - alpha) * prev_y)
            prev_y = smoothed_y
            current_x = win32api.GetCursorPos()[0]
            win32api.SetCursorPos((current_x, smoothed_y))

    else:
        break

s.close()
