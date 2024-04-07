''' 
sudo python3 lidar1.py
'''

import serial
import time

def read_data(ser):
    time.sleep(1)  # Initial sleep to stabilize communication
    #readings_count = 0  # Counter for the readings

    while True:  # Ensures 2 readings are taken
        counter = ser.in_waiting  # Check bytes waiting in the buffer
        if counter > 8:  # Ensure there's enough data for a complete reading
            bytes_serial = ser.read(9)  # Read 9 bytes from LiDAR
            ser.reset_input_buffer()  # Clear buffer to avoid overflow

            # Check if bytes received start with 0x59 0x59 indicating a valid reading
            if bytes_serial[0] == 0x59 and bytes_serial[1] == 0x59:
                distance = bytes_serial[2] + bytes_serial[3] * 256  # Calculate distance
                return distance
                time.sleep(1)  # Sleep to allow some time between readings
                #break
                
def calculate_and_display_movement(ser):
    prev_distance = read_data(ser)
    ser.reset_input_buffer()

    # Loop for continuous monitoring with minimal delay
    while True:
        # Read the next distance
        current_distance = read_data(ser)
        print(f"Current Distance: {current_distance}cm")
        ser.reset_input_buffer()

        # Calculate difference and determine direction, without unnecessary delays
        distance_diff = current_distance - prev_distance
        direction = "didn't move"
        if prev_distance > current_distance:
            direction = "moved closer"
        elif prev_distance < current_distance:
            direction = "moved away"

        print(f"Difference: {distance_diff}cm - {direction}")

        # Update previous distance for the next iteration
        prev_distance = current_distance

        time.sleep(1)

def main():
    ser = serial.Serial("/dev/ttyS0", 115200)
    try:
        if not ser.isOpen():
            ser.open()
        
        print("Place your hand at the origin")
        
        time.sleep(3)

        print("Start moving your hand")
        time.sleep(1)
        
        calculate_and_display_movement(ser)

    except KeyboardInterrupt:
        print("Program interrupted by the user")
    finally:
        if ser is not None:
            ser.close()

if __name__ == "__main__":
    main()
