from json import load
from time import sleep


def restore(sp):
    backup = load(open("backup/liked-songs.json", "r"))

    ids = [item["id"] for item in reversed(backup)]

    for i, song_id in enumerate(ids):
        print(f"Restoring song: {i + 1} of {len(ids) + 1}")
        sp.current_user_saved_tracks_add([song_id])
        sleep(1)
