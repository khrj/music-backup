# Spotify backup

Backup spotify liked songs and playlists to transfer them to a different account

> **NOTE: Restoring only restores liked songs, WIP for playlist restore**

Features:

-   Keeps order of liked songs
-   Backs up playlists

> Note: Until spotify approves an application for this app's client ID, you will
> have to use your own client ID, which you can generate by going to
> https://developer.spotify.com/dashboard/applications, and then substituting
> into the beginning of main.py

## Usage

Install dependencies:

```
poetry install
```

Then run:

```bash
poetry run python src/main.py
```

## Time taken

-   Backup: 1 second for every ~120 songs
-   Restore: 1 second per song
-   Quick restore (loss of order): Nearly instantaneous
-   Clean library: Nearly instantaneous


## Backwards compatibility

If you have an old `backup.json`, rename it to `liked-songs.json` and place it
under a new directory, `backup`