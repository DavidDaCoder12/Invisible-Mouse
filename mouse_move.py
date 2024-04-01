import serial
import pyautogui
import time

ser = serial.Serial("/dev/ttyS0", 115200)
sensitivity = 5

def move(vert, hori):
    vert = vert * sensitivity
    hori = hori * sensitivity

    pyautogui.moveRel(hori, vert, duration=0.02)

def get_reference():
    print("Please remove any objects from the workspace.\n The program will get a reference point in 3")
    time.sleep(1)
    print("2")
    time.sleep(1)
    print("1")
    time.sleep(1)
    print("Reference point taken.")
    return get_dist()

def get_dist():
    while True:
        counter = ser.in_waiting # count the number of bytes of the serial port
        if counter > 8:
            bytes_serial = ser.read(9)
            ser.reset_input_buffer()

            if bytes_serial[0] == 0x59 and bytes_serial[1] == 0x59:  # python3
                distance = bytes_serial[2] + bytes_serial[3] * 256
                return (0, distance)

def main():
    vertical_reference, horizontal_reference = get_reference() #We first get a reference point from the user so we know when their hand is not there.
    while True:
        curr_vert, curr_hori = get_dist()
        if ((curr_vert == vertical_reference) and (curr_hori == horizontal_reference)): #Wait for an object to be placed in the vision of the LiDar sensors
            continue
        else:
            vert_change, hori_change = get_dist()
            if (vert_change == vertical_reference and hori_change == horizontal_reference):
                continue
            move(vert_change, hori_change)