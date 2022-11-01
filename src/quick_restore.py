from json import load
from os import listdir


def quick_restore(sp):
    liked_songs = load(open("backup/liked-songs.json", "r"))

    ids = [item["id"] for item in reversed(liked_songs)]
    batches = [ids[i : i + 50] for i in range(0, len(ids), 50)]

    for batch in batches:
        sp.current_user_saved_tracks_add(batch)

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
