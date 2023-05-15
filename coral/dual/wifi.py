import socket
import signal
from datetime import datetime

# General considerations
# - avoid verbose message formats like json and xml
# - prefer binary message formats

# References:
# - https://docs.python.org/3/library/socket.html
# - https://docs.python.org/3/library/socket.html#example

# We want to create a server on the device running this script
# Here, we define the parameters of this server
HOST = '192.168.1.36'  # The IP address of the ethernet interface
PORT = 8090  # The IP port of the application

# Store data received from clients
buffer = []

# Create a socket object with options:
# - socket.AF_INET: For use with Internet protocols (WiFi, LTE, Ethernet)
# - socket.SOCK_STREAM: Creates a stream socket (INET socket only, UDP protocol only)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    # Bind the socket to a specific address and port
    s.bind((HOST, PORT))

    # Listen for incoming connections
    # Accept maximum 1 connection at the same time
    s.listen(1)

    print('Listening for incoming connections')

    # Define a signal handler to catch the SIGINT signal
    def signal_handler(sig, frame):
        print('Stopping server...')
        s.close()
        exit(0)

    # Register the signal handler
    signal.signal(signal.SIGINT, signal_handler)

    while True:
        # Wait for a client to connect
        conn, addr = s.accept()

        # print(f'Client connected from {addr[0]}:{addr[1]}')

        # Keep the connection open
        while True:
            # Receive data from the client
            data = conn.recv(1024)

            # If the data is empty, close the connection
            if not data:
                break

            data_str = data.decode()

            print(f'Data received from WIFI: {data_str}')

            # Store the received data
            buffer.append(data_str)

        # Close the connection
        conn.close()
