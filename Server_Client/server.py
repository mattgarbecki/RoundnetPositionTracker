import requests
import socket
import sys
import random
from threading import Thread
import smtplib, ssl, json

clients = []
client_data = dict()

def getDataPoint():
    return [1,1]

def sendData(link, name):
    global client_data
    # SEND TO SERVER
    DATA = {"gamedata": client_data, "name":name}

    port = 465  # For SSL

    # Create a secure SSL context
    context = ssl.create_default_context()

    textdata = ""

    message = 'Subject: {}\n\n{}\n\nText Based Data: \n{}'.format("GAME: " + DATA["name"], DATA["gamedata"], textdata)

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("sportspositiontracker@gmail.com", "hip9og-hEtryw")
        server.sendmail("leawoodmax@gmail.com", "leawoodmax@yahoo.com", message)
        server.quit()
    print("done")


def runServer(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = (socket.gethostbyname(socket.gethostname()), port)
    print('starting up on {} port {}'.format(*server_address))
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(2)
    trds = []
    
    for i in range(2):
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
    
    t = Thread(target=selfHandler)
    trds.append(t)
    t.daemon = True
    t.start()

    for t in trds:
        t.join()

    sock.close()

def selfHandler():
    data = ""
    client_data["host"] = []
    client_data["host"] = data
    return

def clientHandler(c, addr):
    global clients, client_data
    client_data[addr[1]] = []
    print(addr, "is Connected")
    try:
        while True:
            data = c.recv(1024).decode("UTF-8").split("%")
            if not data: 
                break
            elif data[0] == "quit":
                print("Removed client", addr)
                clients.remove(addr)
                return
            
            client_data[addr[1]].append({"text": data[0], "time":data[1]})
            
    except:
        print("Removed client", addr)
        clients.remove(addr)
        return

def manageServer():
    LINK = "http://localhost:3500"

    # GET GAME NAME FROM UI
    NAME = input("game name: ")

    URL = LINK + "/hostgame"
    PORT = random.randint(1, 65535)
    PARAMS = {'name':NAME, 'address':socket.gethostbyname(socket.gethostname()), 'port':PORT} 
    r = requests.post(url = URL, json = PARAMS)

    if r.status_code != 200:
        print("ERROR: No Connection")
        quit()

    runServer(PORT)
    #sendData(LINK, NAME)
    
    URL = LINK + "/remove"
    PARAMS = {'name':NAME}
    r = requests.get(url = URL, json = PARAMS)

    if r.status_code != 200:
        print("ERROR: No Connection")
        quit()

if __name__ == "__main__":
    manageServer()
