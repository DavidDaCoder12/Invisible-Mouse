import smbus
import time

# Constants for the TF-Luna
TF_LUNA_DEFAULT_ADDRESS = 0x10  # Check the device address
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
            print(f"Distance: {distance} cm")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Measurement stopped by user")
    finally:
        bus.close()

if __name__ == "__main__":
    main()
