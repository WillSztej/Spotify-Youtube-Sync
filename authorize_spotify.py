from time import time
import spotipy
from flask import Flask, redirect, session, request
from spotipy.oauth2 import SpotifyOAuth
import os
import dotenv
from dotenv import load_dotenv

# App config
app = Flask(__name__)
auth_code = ''


@app.route('/')
def request_auth():
    request = create_spotify_oauth()
    auth_url = request.get_authorize_url()
    print('auth_url: ' + str(auth_url))
    return redirect(auth_url)


@app.route('/spotify/callback')
def spotify_callback():
    session.clear()
    code = request.args.to_dict().get('code')
    token_info = request.get_access_token(code)
    session['token_info'] = token_info
    return redirect("/test")

@app.route('/test')
def test_write():
    session['token_info'], authorized = verify_token()
    session.modified = True
    if not authorized:
        return redirect('/')

    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))


def verify_token():
    token_valid = False
    token_info = session.get('token_info', {})

    if not (session.get('token_info') is None):
        return token_info, token_valid

    now = int(time.time())
    is_token_expired = session.get('token_info').get('expires_at') - now < 60

    if (is_token_expired):
        response = create_spotify_oauth()
        token_info = response.refresh_access_token(session.get('token_info').get('refresh_token'))

    token_valid = True
    return token_info, token_valid


def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=os.getenv('CLIENT_ID'),
        client_secret=os.getenv('CLIENT_SECRET'),
        redirect_uri='http://127.0.0.1:5000/spotify/callback',
        scope='playlist-modify-public playlist-modify-private'
    )


if __name__ == "__main__":
    app.run()
