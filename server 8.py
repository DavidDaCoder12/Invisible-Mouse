import socket
import struct
import win32api

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("10.255.139.107", 5000))

screen_width = win32api.GetSystemMetrics(0)
screen_height = win32api.GetSystemMetrics(1)
win32api.SetCursorPos((screen_width // 2, screen_height // 2))

cm_per_screen_width = screen_width / 25
cm_per_screen_height = screen_height / 17

try:
    while True:
        data = s.recv(8)
        if data:
            distance_from_origin, identifier = struct.unpack('fi', data)
            print(distance_from_origin, identifier)

            if identifier == 1:
                mapped_x_position = int(distance_from_origin * cm_per_screen_width)
                current_y = win32api.GetCursorPos()[1]
                win32api.SetCursorPos((mapped_x_position, current_y))

            elif identifier == 2:
                current_x = win32api.GetCursorPos()[0]
                mapped_y_position = int(distance_from_origin * cm_per_screen_height)
                win32api.SetCursorPos((current_x, mapped_y_position))
        else:
            break
except Exception as e:
    print("Error:", e)
finally:
    s.close()
