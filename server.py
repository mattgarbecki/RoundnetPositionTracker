import socket
import sys

# Create a TCP/IP socket
print(socket.gethostbyname(socket.gethostname()))
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('129.161.190.186', 10000)
print("starting server")
sock.bind(server_address)
sock.listen(1)
while True:
    # Find connections
    connection, client_address = sock.accept()
    try:
        data = connection.recv(999)
        print(data.decode("UTF-8"))

    except:
        connection.close()