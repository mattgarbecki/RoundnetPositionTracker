import requests
import socket
import sys
from threading import Thread

clients = []
client_data = dict()

def sendData():
    global client_data
    # SEND TO SERVER

def runServer():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = (socket.gethostbyname(socket.gethostname()), 8000)
    print('starting up on {} port {}'.format(*server_address))
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)
    trds = []
    
    for i in range(1):
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

def clientHandler(c, addr):
    global clients, client_data
    client_data[addr] = []
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
            
            client_data[addr].append(data)
            print(data)
    except:
        print("Removed client", addr)
        clients.remove(addr)
        return

if __name__ == "__main__":
    LINK = "http://localhost:3500"

    # GET GAME NAME FROM UI
    NAME = input("game name: ")

    URL = LINK + "/hostgame"
    PARAMS = {'name':NAME, 'address':socket.gethostbyname(socket.gethostname())} 
    r = requests.post(url = URL, json = PARAMS)

    if r.status_code != 200:
        print("ERROR: No Connection")
        quit()

    runServer()
    sendData()
    
    URL = LINK + "/remove"
    PARAMS = {'name':NAME}
    r = requests.get(url = URL, json = PARAMS)

    if r.status_code != 200:
        print("ERROR: No Connection")
        quit()
    
    print(client_data)