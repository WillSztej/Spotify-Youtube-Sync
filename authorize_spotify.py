import os
from dotenv import load_dotenv
import requests
from urllib.parse import urlencode

load_dotenv()

def request_auth():
    scopes = 'playlist-modify-public playlist-modify-private'
    my_client_id = os.getenv("MY_CLIENT_ID")
    provider_url = "https://accounts.spotify.com/authorize"

    params = urlencode({
        'client_id': my_client_id,
        'scope': scopes,
        'redirect_uri': 'http://127.0.0.1:5000/spotify/callback',
        'response_type': 'code'
    })
    url = provider_url + '?' + params
    print('url: ' + url)
    response = requests.get(url)


if __name__ == "__main__":
    request_auth()
