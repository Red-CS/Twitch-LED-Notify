import json
import requests

class Refresh():
    """Refreshes Credential Keys and Provides Helper API Methods"""

    def get_access_token():
        keys = json.load(open('./keys.json'))

        url = 'https://id.twitch.tv/oauth2/token'
        data = {
        'client_id' : keys['client_id'],
        'client_secret' : keys['client_secret'],
        'grant_type' : 'client_credentials'
        }

        r = requests.post(url, data=data)
        return r.json()['access_token']