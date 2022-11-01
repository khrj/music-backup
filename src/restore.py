from json import load
from os import listdir
from time import sleep


def restore(sp, quick=False):
    print(f"Restoring liked songs...")
    liked_songs = load(open("backup/liked-songs.json", "r"))
    ids = [item["id"] for item in reversed(liked_songs)]

    if quick:
        batches = [ids[i : i + 50] for i in range(0, len(ids), 50)]
        for batch in batches:
            sp.current_user_saved_tracks_add(batch)
    else:
        for i, song_id in enumerate(ids):
            print(f"Restoring song: {i + 1} of {len(ids)}")
            sp.current_user_saved_tracks_add([song_id])
            sleep(1)

    print(f"Restoring playlists...")
    playlists = (
        [
            load(open(f"backup/playlists/owned/{playlist}", "r"))
            for playlist in listdir("backup/playlists/owned")
        ]
        + [
            load(open(f"backup/playlists/collaborative/{playlist}", "r"))
            for playlist in listdir("backup/playlists/collaborative")
        ]
        + [
            load(open(f"backup/playlists/followed/{playlist}", "r"))
            for playlist in listdir("backup/playlists/followed")
        ]
    )

    user_id = sp.me()["id"]

    for playlist in playlists:
        if playlist["type"] == "followed":
            try:
                sp.current_user_follow_playlist(playlist["id"])
            except:
                print(f"Couldn't follow playlist: ${playlist['name']}")
        else:
            new_playlist = sp.user_playlist_create(
                user_id,
                playlist["name"],
                public=playlist["public"],
                collaborative=playlist["type"] == "collaborative",
                description=playlist["description"],
            )

            ids = [track["id"] for track in playlist["tracks"]]
            batches = [ids[i : i + 50] for i in range(0, len(ids), 50)]

            for batch in batches:
                sp.user_playlist_add_tracks(user_id, new_playlist["id"], batch)

    print(f"Restoring saved albums...")
    saved_albums = load(open("backup/saved-albums.json", "r"))

    ids = [item["id"] for item in saved_albums]
    batches = [ids[i : i + 50] for i in range(0, len(ids), 50)]

    for batch in batches:
        sp.current_user_saved_albums_add(batch)

    print(f"Restoring artists...")
    followed = load(open("backup/followed-artists.json", "r"))

    ids = [item["id"] for item in followed]
    batches = [ids[i : i + 50] for i in range(0, len(ids), 50)]

    for batch in batches:
        sp.user_follow_artists(batch)
