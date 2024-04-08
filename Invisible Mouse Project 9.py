import serial
import time
import struct

def read_data(ser):
    time.sleep(.2)
    while True:
        counter = ser.in_waiting
        if counter > 8:
            bytes_serial = ser.read(9)
            ser.reset_input_buffer()
            if bytes_serial[0] == 0x59 and bytes_serial[1] == 0x59:
                distance = bytes_serial[2] + bytes_serial[3] * 256
                return distance

def calculate_and_display_movement(ser, callback):
    prev_distance = read_data(ser)
    ser.reset_input_buffer()

    while True:
        current_distance = read_data(ser)
        # Here, use the callback instead of print
        if callback:  # Check if callback is provided
            callback(current_distance, prev_distance)
        prev_distance = current_distance
        time.sleep(.2)

def main(callback=None):  # Accept a callback argument
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
