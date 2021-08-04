import os
from flask import Flask
from flask import request

app = Flask(__name__)


@app.route("/spotify/callback")
def spotify_callback():
    content = request.args.to_dict()
    os.environ["AUTH_CODE"] = content.get('code')
    return content.get('code')

if __name__ == '__main__':
    app.run()
