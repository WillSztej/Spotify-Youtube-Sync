import time
import spotipy
from flask import Flask, redirect, session, request
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import os
import dotenv
from dotenv import load_dotenv

# App config
app = Flask(__name__)
auth_code = ''

app.secret_key = 'SOMETHING-RANDOM'
app.config['SESSION_COOKIE_NAME'] = 'spotify-login-session'


@app.route('/')
def request_auth():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    print('auth_url: ' + str(auth_url))
    return redirect(auth_url)


@app.route('/spotify/callback')
def spotify_callback():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info
    return redirect('/test')


@app.route('/test')
def test_write():
    session['token_info'], authorized = verify_token()
    session.modified = True
    print("authorized: " + str(authorized))
    if not authorized:
        return redirect('/')

    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    user_id = sp.me()['id']
    sp.user_playlist_create(user_id, "spotify_playlist", True, False, "this playlist was made with code!")
    return "Playlist has been created!"


def verify_token():
    token_valid = False
    token_info = session.get('token_info', {})

    if not (session.get('token_info', False)):
        return token_info, token_valid

    now = int(time.time())
    is_token_expired = session.get('token_info').get('expires_at') - now < 60

    if is_token_expired:
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(session.get('token_info').get('refresh_token'))

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
