import socket
import time
import threading
import sys
import serial

# IP address and port of the PC
PC_IP = '192.168.34.20'
PC_PORT = 88932  # Arbitrary number
ser = serial.Serial("/dev/ttyS0", 115200)

def get_dist():
    while True:
        counter = ser.in_waiting # count the number of bytes of the serial port
        if counter > 8:
            bytes_serial = ser.read(9)
            ser.reset_input_buffer()

            if bytes_serial[0] == 0x59 and bytes_serial[1] == 0x59:  # python3
                distance = bytes_serial[2] + bytes_serial[3] * 256
                return (0, distance)

# Initialize TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to PC
s.connect((PC_IP, PC_PORT))

def send_data():

    #get data
    hori, vert = get_dist()

    #encode mouse movement data
    message = f'{hori},{vert}'.encode()

    # Send data
    s.sendall(message)

    # Print sent message
    print(f'Sent: {message}')

    # Simulated delay to prevent miscommunication
    time.sleep(0.005)

def wait_for_esc():

    while True:
        #repeatedly check for user to send 
        key = input("Press Escape (Esc) to stop sending data: ").lower()
        if key == 'escape':
            break

    # Close the connection
    s.close()
    print("Connection ended.")
    sys.exit()

# Use threading to avoid time-related issues: one thread waits for Escape to be inputted while the other sends data
thread1 = threading.Thread(target=send_data)
thread1.start()

thread2 = threading.Thread(target=wait_for_esc)
thread2.start()

thread1.join()
thread2.join()