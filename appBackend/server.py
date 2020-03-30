import requests
import socket
import sys
import random
import smtplib, ssl, json

urls = json.loads(open('./endpoints.json').read())

def getData():
    return [1,1]

"""
def sendData(link, name):
    # SEND TO SERVER
    DATA = {"gamedata": user_data, "name":name}

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
"""

def manageApp():

    # api url
    apiAddress = "http://localhost:3500"

    # somehow get this data from kivy
    NAME = input("user name: ")
    HOST = input('host (1 or 0): ')
    game_id = -1

    if HOST == "0":
        player_count = int(input("how many? "))
        PARAMS = {'player_count': player_count} 
        res = requests.post(url = apiAddress + "/createGame", json = PARAMS)
        game_id = json.loads(json.loads(res.text))["id"]

        if res.status_code != 200:
            print("ERROR: No Connection")
            quit()

    else:
        game_id = input("game id: ")

    complete_data = [1,2,3,4]

    PARAMS = {'id': game_id, 'name': NAME, 'data': complete_data} 
    res = requests.post(url = apiAddress + "/sendToGame", json = PARAMS)


if __name__ == "__main__":
    manageApp()
