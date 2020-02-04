import requests
import socket
import sys
from threading import Thread

clients = []

def clientHandler(c, addr):
    global clients
    print(addr, "is Connected")
    try:
        while True:
            data = c.recv(1024).decode("UTF-8")
            if not data: 
                break
            elif data == "quit":
                print("Removed client", addr)
                clients.remove(addr)
                return
            
            # TRANSMIT POSITION DATA TO WHEREVER HERE
            print(data)
    except:
        print("Removed client", addr)
        clients.remove(addr)
        return

if __name__ == "__main__":
    URL = "http://localhost:3500/hostgame"
    NAME = "max"
    PARAMS = {'name':NAME, 'address':socket.gethostbyname(socket.gethostname())} 
    r = requests.post(url = URL, json = PARAMS)

    # ERROR HANDLING FOR POST

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = (socket.gethostbyname(socket.gethostname()), 8000)
    print('starting up on {} port {}'.format(*server_address))
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(5)
    trds = []
    
    for i in range(5):
        try:
            c, addr = sock.accept() 
            clients.append(addr)
            t = Thread(target=clientHandler, args = (c, addr))
            trds.append(t)
            t.daemon = True
            t.start()
        except:
            print("Keyboard Interupt, goodbye")
            break

    for t in trds:
        t.join()
    
    sock.close()