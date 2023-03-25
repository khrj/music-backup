import os
import spotipy
import argparse

from spotipy.oauth2 import SpotifyPKCE
from backup import backup
from clean_library import clean_library
from restore import restore

client_id = "d93f79db5bbb41999a52734b9c95585a"
redirect_uri = "http://localhost:3000/authed"
scope = " ".join(
    [
        "user-library-read",
        "user-library-modify",
        "playlist-read-private",
        "playlist-read-collaborative",
        "playlist-modify-private",
        "playlist-modify-public",
        "user-follow-read",
        "user-follow-modify",
    ]
)

auth_manager = SpotifyPKCE(
    scope=scope,
    client_id=client_id,
    redirect_uri=redirect_uri,
)

if not auth_manager.validate_token(auth_manager.get_cached_token()):
    print("If your browser doesn't open automatically, open", auth_manager.get_authorize_url())

sp = spotipy.Spotify(auth_manager=auth_manager)

parser = argparse.ArgumentParser(description="Backup and restore spotify library")
parser.add_argument('--backup', action='store_true')
args = parser.parse_args()

choice = "y" if args.backup else input(f"Logged in as {sp.me()['display_name']}. Continue? [y/n/logout] ")
if choice == "y":
    pass
elif choice == "logout":
    os.remove(".cache")
    quit()
else:
    quit()


choice = "1" if args.backup else input(
    """What would you like to do? Available:
1. Backup
2. Quick restore (doesn't preserve order of liked songs)
3. Restore (preserves order of liked songs)
4. [DANGEROUS] Clean library

Note that while quick restore loses order for liked songs, playlists are always ordered correctly.

[1/2/3/4/q]: """
)

if choice == "1":
    backup(sp)
elif choice == "2":
    restore(sp, True)
elif choice == "3":
    restore(sp, False)
elif choice == "4":
    confirm = input(
        f"[{sp.me()['display_name'].upper()}] This will delete everything in your library, including liked songs, playlists, albums and followed artists. Are you sure you want to continue? [y/n] "
    )
    if confirm == "y":
        clean_library(sp)
    else:
        quit()
else:
    quit()
