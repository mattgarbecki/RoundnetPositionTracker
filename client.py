import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('129.161.190.186', 10000)
print('connecting to %s port %s' % server_address)

while True:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(server_address)
        message=input('Message: ')
        if message=='quit':
            break
        sock.sendall(message.encode("UTF-8"))
    except:
        break
sock.close()