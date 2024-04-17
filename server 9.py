import socket
import struct
import win32api

def main():
    host = "10.255.139.107"
    port = 5000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))
        
        screen_width = win32api.GetSystemMetrics(0)
        screen_height = win32api.GetSystemMetrics(1)
        win32api.SetCursorPos((screen_width // 2, screen_height // 2))

        cm_per_screen_width = screen_width / 25
        cm_per_screen_height = screen_height / 17

        while True:
            data = s.recv(8)
            if not data:
                break
            
            if len(data) == 8:  # Ensure the full packet has been received
                distance_from_origin, identifier = struct.unpack('fi', data)
                print(f"Distance: {distance_from_origin}, Sensor ID: {identifier}")

                if identifier == 1:
                    mapped_x_position = int(distance_from_origin * cm_per_screen_width)
                    current_y = win32api.GetCursorPos()[1]
                    win32api.SetCursorPos((mapped_x_position, current_y))
                elif identifier == 2:
                    mapped_y_position = int(distance_from_origin * cm_per_screen_height)
                    current_x = win32api.GetCursorPos()[0]
                    win32api.SetCursorPos((current_x, mapped_y_position))
    except Exception as e:
        print(f"Error: {e}")
    finally:
        s.close()

if __name__ == '__main__':
    main()
