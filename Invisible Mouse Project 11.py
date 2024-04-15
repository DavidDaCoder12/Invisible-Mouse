import serial
import time
import struct
import pigpio

i2c_bus = 1
lidar_addr = 0x10

pi = pigpio.pi()

handle = pi.i2c_open(i2c_bus, lidar_addr)

def read_data(ser, pi, max_distance = 45.72):
    time.sleep(.02)
    while True:
        data = pi.i2c_read_device(handle, 4)
        
        counter = ser.in_waiting
        if counter > 8 and distance_horizontal != 0:
            bytes_serial = ser.read(9)
            ser.reset_input_buffer()
            if bytes_serial[0] == 0x59 and bytes_serial[1] == 0x59:
                distance = (bytes_serial[2] + bytes_serial[3] * 256) / 1.0
                #Added max distance about 18 inches in centimeters
                if distance > max_distance:
                    continue
                return distance_horizontal, distance_vertical

def calculate_and_display_movement(ser, callback):
    prev_distance = read_data(ser)
    ser.reset_input_buffer()

    while True:
        current_distance = read_data(ser, lidar_addr)
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
