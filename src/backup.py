import re
import unicodedata

from json import dump
from pathlib import Path


def get_useful_info_for_tracks(tracks):
    return [
        {
            "name": item["track"]["name"],
            "artists": [artist["name"] for artist in item["track"]["artists"]],
            "id": item["track"]["id"],
            "isrc": item["track"]["external_ids"]["isrc"],
            "added_at": item["added_at"],
        }
        for item in tracks
    ]


def get_useful_info_for_playlists(playlists, owner_id):
    cleaned = []

    for playlist in playlists:

        playlist_type = None

        if playlist["owner"]["id"] == owner_id or (
            playlist["owner"]["id"] == "spotify"
            and (
                playlist["name"].lower().startswith("your top songs")
                or "for you" in playlist["name"].lower()
            )
        ):
            playlist_type = "owned"
        elif playlist["collaborative"] is True:
            playlist_type = "collaborative"
        else:
            playlist_type = "followed"

        cleaned.append(
            {
                "name": playlist["name"],
                "description": playlist["description"],
                "id": playlist["id"],
                "type": playlist_type,
                "public": playlist["public"],
            }
        )

    return cleaned


def get_all_items(sp, results):
    items = results["items"]

    while results["next"]:
        results = sp.next(results)
        items.extend(results["items"])

    return items


def get_liked_songs(sp):
    songs = get_all_items(sp, sp.current_user_saved_tracks(limit=50))
    return get_useful_info_for_tracks(songs)


def get_playlists(sp):
    playlists = get_all_items(sp, sp.current_user_playlists(limit=50))
    return get_useful_info_for_playlists(playlists, sp.me()["id"])


def get_playlist_tracks(sp, playlist):
    tracks = get_all_items(sp, sp.playlist_tracks(playlist["id"], limit=50))
    return get_useful_info_for_tracks(tracks)


def slugify(value):
    value = (
        unicodedata.normalize("NFKD", str(value))
        .encode("ascii", "ignore")
        .decode("ascii")
    )
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")


def backup(sp):
    print("Backing up... This might take a while")

    Path("backup/playlists/owned").mkdir(parents=True, exist_ok=True)
    Path("backup/playlists/collaborative").mkdir(parents=True, exist_ok=True)
    Path("backup/playlists/followed").mkdir(parents=True, exist_ok=True)

    songs = get_liked_songs(sp)
    playlists = get_playlists(sp)

    for playlist in playlists:
        playlist["tracks"] = get_playlist_tracks(sp, playlist)
        dump(
            playlist,
            open(
                f"backup/playlists/{playlist['type']}/{slugify(playlist['name'])}.json",
                "w",
            ),
        )

    dump(songs, open("backup/liked-songs.json", "w"))

    print("Backup complete!")
    print("* Your liked songs were backed up")
    print("* The following playlists were backed up:")

    for i, playlist in enumerate(playlists):
        print(f"{i + 1}. {playlist['name']}")
