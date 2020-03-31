import requests
#import socket
#import sys
#import random
#import smtplib, ssl
import json
import os.path

urls = json.loads(open('./endpoints.json').read())
data_file = "test_data.json"

def wait_for_null(keys):
    player_data = json.loads(open(os.path.dirname(__file__) + '../' + data_file).read())

    for i in range(len(keys)):
        if player_data[keys[i]] == None:
            player_data = json.loads(open(os.path.dirname(__file__) + '../' + data_file).read())
            i = 0

def manageApp():

    # player information
    NAME = HOST = game_id = player_count = None

    player_data = json.loads(open(os.path.dirname(__file__) + '../' + data_file).read())

    wait_for_null(['name', 'host'])

    NAME = player_data['name']
    HOST = player_data['host']

    # get unique id
    if HOST:
        wait_for_null(['player_count'])
        
        player_count = player_data['player_count']
        PARAMS = {'player_count': player_count} 
        res = requests.post(url = urls['api'] + "/createGame", json = PARAMS)
        game_id = json.loads(json.loads(res.text))["id"]

        if res.status_code != 200:
            print("ERROR: No Connection")
            quit()

    else:
        wait_for_null(['game_id'])
        
        game_id = player_data['game_id']

    # get and send game data

    wait_for_null(['results_data'])

    PARAMS = {'id': game_id, 'name': NAME, 'data': player_data['results_data']} 
    res = requests.post(url = urls['api'] + "/sendToGame", json = PARAMS)


if __name__ == "__main__":
    manageApp()
