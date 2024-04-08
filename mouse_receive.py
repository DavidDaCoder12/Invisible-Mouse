import socket
import pyautogui

sensitivity = 5

def move(vert, hori):
    vert = vert * sensitivity
    hori = hori * sensitivity

    pyautogui.moveRel(hori, vert, duration=0.02)

    # IP address and port to listen on
  
PC_IP = '0.0.0.0'  # Listen to all interfaces
PC_PORT = 88932  # Arbitrary number, same as sender script

# Initialize TCP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the IP address and port
s.bind((PC_IP, PC_PORT))

# Listen for incoming communications
s.listen()

print(f"Listening on {PC_IP}:{PC_PORT}...")

# Accept incoming connection
conn, addr = s.accept()
print(f"Connected to {addr}")

data = conn.recv(512)
decoded_data = data.decode()
h_ref_str, v_ref_str = decoded_data.split(',')
h_ref = int(h_ref_str)
v_ref = int(v_ref_str)

# Receive and print data
while True:
    data = conn.recv(512)  # Receive data (up to 512 bytes)
    if not data:
        break # Close the connection if sender stops

    # Decode data and use it to move the mouse
    decoded_data = data.decode()
    h_str, v_str = decoded_data.split(',')
    h = int(h_str)
    v = int(v_str)



    # Close the connection if Raspberry Pi closes first or no more data is being sent
    conn.close()