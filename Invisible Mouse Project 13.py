'''
sudo python3 lidar2.py
'''

import smbus
import time

# Constants for the TF-Luna
TF_LUNA_DEFAULT_ADDRESS = 0x10  # Device Address
DISTANCE_REGISTER = 0x00  # Register to read distance from

def read_distance(bus):
    # Read two bytes from the distance register
    distance_bytes = bus.read_i2c_block_data(TF_LUNA_DEFAULT_ADDRESS, DISTANCE_REGISTER, 2)
    # Convert the two bytes to an integer
    distance = distance_bytes[0] + (distance_bytes[1] << 8)
    return distance

def main():
    # Create an SMBus instance on I2C bus 1 (pins 3 and 5 on Raspberry Pi)
    bus = smbus.SMBus(1)
    
    try:
        while True:
            distance = read_distance(bus)
            # Convert distance to inches for the check (1 inch = 2.54 cm)
            distance_in_inches = distance / 2.54
            # Check if the distance is less than or equal to 18 inches
            if distance > 45.72:
                continue    
                  
            #distance_in_inches = distance / 2.54
            #print(f"Distance: {distance} cm ({distance_in_inches:.2f} inches)")
            
            return distance
            time.sleep(1)
    except KeyboardInterrupt:
        print("Measurement stopped by user")
    finally:
        bus.close()
