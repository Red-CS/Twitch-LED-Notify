from datetime import datetime as dt
from refresh import Refresh
from write import Write
import requests
import logging
import sys
import time
import webbrowser


# TODO Write function to refresh rewrite access token if it expires
logging.basicConfig(filename='log.log', level=logging.INFO)

class Helix:
    """Connects with New Twitch API"""

    def __init__(self, user_name, client_id, access_token):

        # Initialize api
        self.user_name = user_name
        self.client_id = client_id
        self.access_token = access_token
        self.headers = {
            'Client-ID' : client_id,
            'Authorization' : 'Bearer ' + access_token
        }
    
    def get_streams(self):

        # Get user_id
        url = f'https://api.twitch.tv/helix/users?login={self.user_name}'
        r = requests.get(url, headers=self.headers)
        logging.info(r.json())
        try:
            user_id = r.json()['data'][0]['id']
        except KeyError:
            if r.json()['message'] == 'Invalid OAuth token':
                print("Invalid Oauth token, resetting . . .")
                new_access_token = Refresh.get_access_token()
                print(f"Refreshed Access Token: {new_access_token}")
                print("Writing to './keys.json' . . .")
                Write.write({'access_token': new_access_token}, './keys.json')
                print("Successfully wrote new access token to './keys.json'")
                sys.exit(0)
            else:
                print("An unexpected error occurred")
                sys.exit(1)

        # Get twitch users you follow
        url = f'https://api.twitch.tv/helix/users/follows?from_id={user_id}'
        r = requests.get(url, headers=self.headers)
        data = r.json()
        followed = []
        for streamer in data['data']:
            followed.append(streamer['to_name'])


        # Sort twitch users
        url = 'https://api.twitch.tv/helix/streams?user_login='
        streams = {
            "live" : [],
            "away" : []
        }
        for streamer in followed:
            temp = url + streamer
            r = requests.get(url=temp, headers=self.headers)
            data = r.json()
            if len(data['data']) == 0:
                streams['away'].append(streamer)
            else:
                streams['live'].append(streamer)
        
        # Create return string
        list = "Live:\n"
        for i in streams['live']:
            list += "          {}\n".format(i)
        list += "Away:\n"
        for i in streams['away']:
            list += "          {}\n".format(i)

        return list
                   
    
    def open_stream(self, streamer_name):

        # Opens a new tab in browser to stream of passed streamer
        webbrowser.open(f'https://www.twitch.tv/{streamer_name}')

    def check_stream(self, streamer_name):

        # Check if streamer exists
        url = f'https://api.twitch.tv/helix/users?login={streamer_name}'
        r = requests.get(url=url, headers=self.headers)
        if len(r.json()) == 3:
            return "A streamer with that username could not be found."

        # Checks the status of passed streamer
        url = f'https://api.twitch.tv/helix/streams?user_login={streamer_name}'
        r = requests.get(url=url, headers=self.headers)
        data = r.json()

        if len(data['data']) == 0:    
            return f"{streamer_name} is not live."

        # Parse "started_at" timestamp
        timestamp = [
            int(data['data'][0]['started_at'][8:10]),    # Day
            int(data['data'][0]['started_at'][11:13]),   # Hour
            int(data['data'][0]['started_at'][14:16]),   # Minute
            int(data['data'][0]['started_at'][17:19])    # Second
        ]

        # Translate into elapsed time
        timestamp[0] = int(dt.utcnow().strftime('%d')) - timestamp[0]
        timestamp[1] = int(dt.utcnow().strftime('%H')) - timestamp[1]
        timestamp[2] = int(dt.utcnow().strftime('%M')) - timestamp[2]
        timestamp[3] = int(dt.utcnow().strftime('%S')) - timestamp[3]

        logging.info(timestamp)

        str_duration = []
        if timestamp[0] != 0:
            str_duration.append(f"{str(timestamp[0])} days")
        if timestamp[1] != 0:
            str_duration.append(f"{str(timestamp[1])} hours")
        if timestamp[2] != 0:
            str_duration.append(f"{str(timestamp[2])} minutes")
        if timestamp[3] != 0:
            str_duration.append(f"{str(timestamp[3])} seconds")
        
        for i in range(len(str_duration)):
            live_message = f"""{streamer_name} is live!

          Title . . . . . . . . . . {data["data"][0]["title"]}
          Viewer Count . . . . . . . . . . {data["data"][0]["viewer_count"]}
          Start Time . . . . . . . . . . Some time ago

          """
          # TODO Change Start Time to Stream Duration
            return live_message