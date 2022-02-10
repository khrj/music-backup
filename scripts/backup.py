import json
import os

import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyPKCE

load_dotenv()

CLIENT_ID = "d93f79db5bbb41999a52734b9c95585a"
REDIRECT_URI = "http://localhost:3000/authed"


def get_liked_songs(sp):
    results = sp.current_user_saved_tracks(limit=50)
    songs = results['items']
    while results['next']:
        results = sp.next(results)
        songs.extend(results['items'])
    return songs


def clean_results(results):
    cleaned = []

    for item in results:
        cleaned.append({
            "name": item["track"]["name"],
            "artists": list(map(lambda artist: artist["name"], item["track"]["artists"])),
            "id": item["track"]["id"],
            "added_at": item["added_at"],
        })

    return cleaned


def main():
    scope = "user-library-read"
    sp = spotipy.Spotify(
        auth_manager=SpotifyPKCE(scope=scope, client_id=CLIENT_ID, redirect_uri="http://localhost:3000/authed"))

    choice = input("Backing up from " + sp.me()["display_name"] + ". Continue? [y/n/logout] ")

    if choice == "y":
        pass
    elif choice == "logout":
        os.remove(".cache")
        quit()
    else:
        quit()

    results = get_liked_songs(sp)
    cleaned_results = clean_results(results)

    json.dump(cleaned_results, open('backup.json', 'w'))

    for idx, item in enumerate(cleaned_results):
        print(idx + 1, item["name"], "–", ", ".join(item["artists"]))


main()
