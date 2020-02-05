import requests
import socket
import time

def runClient(address):
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

if __name__ == "__main__":
    LINK = "http://localhost:3500"
    URL = LINK + "/address"

    # PIPE UI INPUT HERE FOR GAME NAME
    NAME = input("game name: ")
    PARAMS = {'name':NAME} 
    r = requests.get(url = URL, params = PARAMS)

    if r.status_code != 200:
        print("ERROR: No Connection")
        quit()

    if r.text == "NONAME" or r.text == "INVALID":
        print("ERROR: gamename not found")
        quit()

    runClient(r.text)
