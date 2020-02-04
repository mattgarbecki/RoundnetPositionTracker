import requests
import socket


if __name__ == "__main__":
    URL = "http://localhost:3500/address"
    PARAMS = {'name':"max"} 
    r = requests.get(url = URL, params = PARAMS)

    # ERROR HANDLING FOR GET

    address = r.text

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = (address, 8000)
    print('connecting to {} port {}'.format(*server_address))
    sock.connect(server_address)

    while True:
        # CHANGE MESSAGE TO BE THE DATA THATS SENDING
        message = input()
        if message == "quit":
            print("Closing client")
            sock.sendall("quit".encode("UTF-8"))
            break
        sock.sendall(message.encode("UTF-8"))

    sock.close()