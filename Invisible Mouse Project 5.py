''' 
sudo python3 lidar1.py
'''

import serial
import time

def read_data(ser):
    time.sleep(1)  # Initial sleep to stabilize communication
    readings_count = 0  # Counter for the readings

    while readings_count < 2:  # Ensures 2 readings are taken
        counter = ser.in_waiting  # Check bytes waiting in the buffer
        if counter > 8:  # Ensure there's enough data for a complete reading
            bytes_serial = ser.read(9)  # Read 9 bytes from LiDAR
            ser.reset_input_buffer()  # Clear buffer to avoid overflow

            # Check if bytes received start with 0x59 0x59 indicating a valid reading
            if bytes_serial[0] == 0x59 and bytes_serial[1] == 0x59:
                distance = bytes_serial[2] + bytes_serial[3] * 256  # Calculate distance
                #print("Distance: " + str(distance) + "cm")
                readings_count += 1  # Increment the reading counter
                return distance
                time.sleep(1)  # Sleep to allow some time between readings
                #break

def main():
    ser = serial.Serial("/dev/ttyS0", 115200)
    try:
        if not ser.isOpen():
            ser.open()

        print("bruh")
        for i in range(2):
            distance = read_data(ser)
            print("Distance: " + str(distance) + "cm")

    except KeyboardInterrupt:
        print("Program interrupted by the user")
    finally:
        if ser is not None:
            ser.close()

if __name__ == "__main__":
    main()
