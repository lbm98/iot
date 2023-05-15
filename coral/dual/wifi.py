def listen_on_ip_socket():
    # Create a socket object using the following options:
    # - socket.AF_INET: For use with IP
    # - socket.SOCK_STREAM: Creates a stream socket (INET socket only, UDP protocol only)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    sock.bind((HOST, PORT))

    # Listen for incoming connections
    # Accept maximum 1 connection at the same time
    sock.listen(1)

    print(f"Listening on {HOST}:{PORT}")