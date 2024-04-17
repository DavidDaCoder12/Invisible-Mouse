'''
sudo python3 lidar3.py
'''
#UART
import serial
import time
import struct

def read_data(ser, max_distance = 45.72):
    time.sleep(0.01)
    while True:
        counter = ser.in_waiting
        if counter > 8:
            bytes_serial = ser.read(9)
            ser.reset_input_buffer()
            if bytes_serial[0] == 0x59 and bytes_serial[1] == 0x59:
                distance = (bytes_serial[2] + bytes_serial[3] * 256) / 1.0
                #Added max distance about 18 inches in centimeters
                if distance > max_distance:
                    continue
                return distance

def calculate_and_display_movement(ser, callback):
    prev_distance = read_data(ser)
    ser.reset_input_buffer()

    while True:
        current_distance = read_data(ser)
        if callback:  # Check if callback is provided
            callback(current_distance, prev_distance)
        prev_distance = current_distance
        time.sleep(0.01)

def main(callback=None):  # Accept a callback argument
    # Pin for GPIO 14 and 15
    ser = serial.Serial("/dev/ttyS0", 115200)
    try:
        if not ser.isOpen():
            ser.open()

        # Pass the callback to your movement function
        calculate_and_display_movement(ser, callback)

    except KeyboardInterrupt:
        print("Program interrupted by the user")
    finally:
        if ser is not None:
            ser.close()
