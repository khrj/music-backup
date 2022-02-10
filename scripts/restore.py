import json
import os
import time

import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyPKCE

load_dotenv()

CLIENT_ID = "d93f79db5bbb41999a52734b9c95585a"
REDIRECT_URI = "http://localhost:3000/authed"


def main():
    scope = "user-library-modify"
    sp = spotipy.Spotify(
        auth_manager=SpotifyPKCE(scope=scope, client_id=CLIENT_ID, redirect_uri="http://localhost:3000/authed"))

    choice = input("Restoring to " + sp.me()["display_name"] + ". Continue? [y/n/logout] ")

    if choice == "y":
        pass
    elif choice == "logout":
        os.remove(".cache")
        quit()
    else:
        quit()

    backup = json.load(open("backup.json", "r"))
    ids = list(map(lambda item: item["id"], backup))

    ids.reverse()

    for idx, song_id in enumerate(ids):
        print(idx)
        sp.current_user_saved_tracks_add([song_id])
        time.sleep(1)


main()
