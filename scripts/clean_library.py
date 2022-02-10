import json
import os

import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyPKCE

load_dotenv()

CLIENT_ID = "d93f79db5bbb41999a52734b9c95585a"
REDIRECT_URI = "http://localhost:3000/authed"


def chunks(lst, chunk_size):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]


def main():
    scope = "user-library-modify"
    sp = spotipy.Spotify(
        auth_manager=SpotifyPKCE(scope=scope, client_id=CLIENT_ID, redirect_uri="http://localhost:3000/authed"))

    choice = input("WARNING: Deleting all liked songs of " + sp.me()["display_name"] + ". Continue? [y/n/logout] ")

    if choice == "y":
        pass
    elif choice == "logout":
        os.remove(".cache")
        quit()
    else:
        quit()

    backup = json.load(open("backup.json", "r"))
    ids = list(map(lambda item: item["id"], backup))
    batches = list(chunks(ids, 50))

    for batch in batches:
        sp.current_user_saved_tracks_delete(batch)


main()
