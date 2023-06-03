from spotipy import Spotify
from pathlib import Path

from backup import (
    get_useful_info_for_playlists,
    get_playlist_tracks,
    slugify,
    write,
)

def get_playlists(sp: Spotify, user_id: str):
    results = sp.user_playlists(user=user_id, limit=50)
    items = results["items"]

    while len(results["items"]) > 0:
        results = sp.user_playlists(user=user_id, limit=50, offset=results["offset"] + 50)
        items.extend(results["items"])

    return get_useful_info_for_playlists(items, sp.me()["id"])


def save_profile(sp: Spotify, user_link: str):
    user_id = user_link.removeprefix("https://open.spotify.com/user/")
    user = sp.user(user_id) 
    slug = slugify(user["display_name"])

    Path(f"backup/people/{slug}/playlists/").mkdir(parents=True, exist_ok=True)
    
    print("Backing up playlists...")
    playlists, blends = get_playlists(sp, user_id)

    for playlist in playlists:
        playlist["tracks"] = get_playlist_tracks(sp, playlist)
        write(
            playlist,
            f"backup/people/{slug}/playlists/{slugify(playlist['name'])}-{slugify(playlist['id'])}.json",
        )

    write(blends, f"backup/people/{slug}/blend-names.json")