import re
import unicodedata
import subprocess

from json import dump
from spotipy import Spotify
from pathlib import Path
from tabulate import tabulate
from shutil import rmtree


def get_useful_info_for_tracks(tracks):
    return [
        {
            "name": item["track"]["name"],
            "artists": [artist["name"] for artist in item["track"]["artists"]],
            "release_date": item["track"]["album"]["release_date"],
            "id": item["track"]["id"],
            "isrc": item["track"]["external_ids"].get("isrc"),
            "added_at": item["added_at"],
        }
        for item in tracks
        if item["track"]
    ]


def get_useful_info_for_playlists(playlists, owner_id):
    cleaned = []
    blends = []

    for playlist in playlists:
        if playlist["description"].startswith("A blend of music for"):
            blends.append(playlist["name"].split(" + "))
            continue

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
                "owner": {
                    "display_name": playlist["owner"]["display_name"],
                    "id": playlist["owner"]["id"],
                },
                "type": playlist_type,
                "public": playlist["public"],
            }
        )

    return cleaned, blends


def get_useful_info_for_albums(albums):
    return [
        {
            "name": album["album"]["name"],
            "artists": [artist["name"] for artist in album["album"]["artists"]],
            "id": album["album"]["id"],
            "upc": album["album"]["external_ids"]["upc"],
            "added_at": album["added_at"],
        }
        for album in albums
    ]


def get_useful_info_for_followed(artists):
    return [
        {
            "name": artist["name"],
            "id": artist["id"],
        }
        for artist in artists
    ]


def get_all_items(sp: Spotify, results, key=None):
    items = results["items"]

    while results["next"]:
        results = sp.next(results)
        if key:
            results = results[key]
        items.extend(results["items"])

    return items


def get_liked_songs(sp: Spotify):
    results = sp.current_user_saved_tracks(limit=50)
    items = results["items"]

    while len(results["items"]) > 0:
        results = sp.current_user_saved_tracks(limit=50, offset=results["offset"] + 50)
        items.extend(results["items"])

    return get_useful_info_for_tracks(items)


def get_playlists(sp: Spotify):
    results = sp.current_user_playlists(limit=50)
    items = results["items"]

    while len(results["items"]) > 0:
        results = sp.current_user_playlists(limit=50, offset=results["offset"] + 50)
        items.extend(results["items"])

    return get_useful_info_for_playlists(items, sp.me()["id"])


def get_albums(sp: Spotify):
    albums = get_all_items(sp, sp.current_user_saved_albums(limit=50))
    return get_useful_info_for_albums(albums)


def get_followed_artists(sp: Spotify):
    artists = get_all_items(
        sp, sp.current_user_followed_artists(limit=50)["artists"], "artists"
    )
    return get_useful_info_for_followed(artists)


def get_playlist_tracks(sp: Spotify, playlist):
    results = sp.playlist_tracks(playlist["id"], limit=50)
    items = results["items"]

    while len(results["items"]) > 0:
        results = sp.playlist_tracks(
            playlist["id"], limit=50, offset=results["offset"] + 50
        )
        items.extend(results["items"])

    return get_useful_info_for_tracks(items)


def slugify(value):
    value = (
        unicodedata.normalize("NFKD", str(value))
        .encode("ascii", "ignore")
        .decode("ascii")
    )
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")


def write(data, path):
    dump(data, open(path, "w"), indent="\t")


def backup(sp: Spotify, playlist_name=None):
    print("Backing up... This might take a while")

    backup = Path("backup")
    backup.mkdir(parents=True, exist_ok=True)

    if not playlist_name:
        git_status = subprocess.run(
            ["git", "status", "--porcelain"], cwd=backup, capture_output=True, text=True
        )

        if git_status.returncode != 0:
            subprocess.run(["git", "init"], cwd=backup).check_returncode()

        if git_status.stdout:
            print("You have uncommitted changes in backup/, exiting")
            exit(1)

        subprocess.run(["git", "pull"], cwd=backup).check_returncode()

        rmtree("backup/playlists", ignore_errors=True)
        Path("backup/liked-songs.json").unlink(missing_ok=True)
        Path("backup/saved-albums.json").unlink(missing_ok=True)
        Path("backup/followed-artists.json").unlink(missing_ok=True)
        Path("backup/blend-names.json").unlink(missing_ok=True)

    Path("backup/playlists/owned").mkdir(parents=True, exist_ok=True)
    Path("backup/playlists/collaborative").mkdir(parents=True, exist_ok=True)
    Path("backup/playlists/followed").mkdir(parents=True, exist_ok=True)

    if not playlist_name:
        print("Backing up liked songs...")
        songs = get_liked_songs(sp)
        write(songs, "backup/liked-songs.json")

        print("Backing up albums...")
        albums = get_albums(sp)
        write(albums, "backup/saved-albums.json")

        print("Backing up followed artists...")
        followed = get_followed_artists(sp)
        write(followed, "backup/followed-artists.json")

    print("Backing up playlists...")
    playlists, blends = get_playlists(sp)
    for playlist in playlists:
        if playlist_name and playlist["name"] != playlist_name:
            continue

        playlist["tracks"] = get_playlist_tracks(sp, playlist)
        write(
            playlist,
            f"backup/playlists/{playlist['type']}/{slugify(playlist['name'])}-{slugify(playlist['id'])}.json",
        )

    if not playlist_name:
        write(blends, "backup/blend-names.json")

        print("Commiting and pushing changes...")

        subprocess.run(["git", "add", "."], cwd=backup).check_returncode()

        subprocess.run(
            "git diff-index --quiet HEAD || git commit -m 'Automated update'",
            cwd=backup,
            shell=True,
        ).check_returncode()

        subprocess.run(["git", "push"], cwd=backup)

        print("Backup complete!")
        print("* Your liked songs were backed up")
        print("* Your followed artists were backed up")
        print("* Your saved albums were backed up")
        print("* Names of people in blends were backed up (excluding large blends)")
        print("* The following playlists were backed up:")

        print(
            tabulate(
                [[x["name"], x["type"]] for x in playlists],
                headers=["Name", "Type"],
                showindex=range(1, len(playlists) + 1),
            )
        )
