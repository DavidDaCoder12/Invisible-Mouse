import socket

def main():
    host = "10.84.124.40"
    port = 5000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))

        while True:
            # Receive a chunk of data
            data = s.recv(1024)  # Increase buffer size to handle longer strings
            if not data:
                break  # Exit the loop if no data is received (connection closed)

            # Decode the received bytes into a string
            message = data.decode('utf-8')
            print(f"Received: {message.strip()}")  # Print the received message, strip any newlines or extra spaces

    except Exception as e:
        print(f"Error: {e}")
    finally:
        s.close()

if __name__ == '__main__':
    main()
