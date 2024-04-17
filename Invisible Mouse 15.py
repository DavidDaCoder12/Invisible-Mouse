import smbus
import time

# Constants for the TF-Luna
TF_LUNA_DEFAULT_ADDRESS = 0x10  # Device Address
DISTANCE_REGISTER = 0x00  # Register to read distance from
max_distance = 45.72  # Maximum distance to monitor in centimeters ( 18 inches)

def read_distance(bus, max_distance = 36.00, min_distance = 10.00):
    time.sleep(0.2)
    while True:
        # Read two bytes from the distance register
        distance_bytes = bus.read_i2c_block_data(TF_LUNA_DEFAULT_ADDRESS, DISTANCE_REGISTER, 2)
        # Convert the two bytes to an integer
        distance = distance_bytes[0] + (distance_bytes[1] << 8) / 1.0

        if min_distance > distance > max_distance:
            continue    
        return distance
        
def calculate_and_display_movement(bus, callback):
    prev_distance = read_distance(bus)  # Initial read to set the previous distance

    while True:
        current_distance = read_distance(bus)
        if callback:  # Check if callback is provided
            callback(current_distance, prev_distance)
        prev_distance = current_distance
        time.sleep(0.2)  # Delay to prevent excessive I2C traffic and CPU usage

def main(callback=None):
    # Create an SMBus instance on I2C bus 1 (pins 3 and 5 on Raspberry Pi)
    bus = smbus.SMBus(1)
    
    try:
        # Pass the callback function to calculate_and_display_movement
        calculate_and_display_movement(bus, callback)
    except KeyboardInterrupt:
        print("Program interrupted by the user")
    finally:
        bus.close()
