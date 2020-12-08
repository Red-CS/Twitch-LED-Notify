import time
import serial
from helix import Helix
import json
import requests
import sys

serialcomm = serial.Serial('COM5', 115200)
serialcomm.timeout = 1

keys = json.load(open('./keys.json'))

api = Helix(
        user_name = keys['username'],
        client_id = keys['client_id'],
        access_token = keys['access_token'])

while True:

    # Get list of followed streamers
    url = 'https://api.twitch.tv/helix/users/follows?from_id=' #TODO Change to get id dynamically
    # sys.exit(1)
    r = requests.get(url, headers=api.headers)
    followed = []
    for streamer in r.json()['data']:
        followed.append(streamer['to_name'])


    url2 = 'https://api.twitch.tv/helix/streams?user_login='
    for streamer in followed:
        r2 = requests.get(url=url2 + streamer, headers=api.headers)
        
        if len(r2.json()['data']) == 0:
            # print(f'{streamer} is away')
            i = 'off'
        else:
            # print(f'{streamer} is live!')
            i = 'on'
            break

    serialcomm.write(i.encode())

    # print(serialcomm.readline().decode('ascii'))

    if i == 'on':
        time.sleep(60)
    elif i == 'off':
        time.sleep(3)
    # Take cmd input to stop code from running

serialcomm.close()