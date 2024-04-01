import serial
import time
ser = serial.Serial("/dev/ttyS0", 115200)
# we define a new function that will get the data from LiDAR and publish it
def read_data():
    time.sleep(1) # 1000 ms  
    while True:
        counter = ser.in_waiting # count the number of bytes of the serial port
        if counter > 8:
            bytes_serial = ser.read(9)
            ser.reset_input_buffer()

            if bytes_serial[0] == 0x59 and bytes_serial[1] == 0x59:  # python3
                distance = bytes_serial[2] + bytes_serial[3] * 256
                print("Distance: " + str(distance) + "cm")
                break
            
if __name__ == "__main__":
    try:
        if ser.isOpen() == False:
            ser.open()
        read_data()
    except KeyboardInterrupt:
        if ser != None:
            ser.close()
            print("program interrupted by the user")
