# Spotify backup

Backup spotify liked songs and playlists to transfer them to a different account

Features:

-   Backs up liked songs
    -   Keeps order of liked songs
-   Backs up albums
-   Backs up playlists (followed, collaborative and created)
    -   Re-follows playlists on restore
    -   Recreates collaborative and created playlists

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

> **Quick restore causes liked songs to lose order. Playlists are always ordered
> correctly.**

-   Backup: 1 second for every ~120 songs
-   Restore: 1 second per liked song, 1 second for every ~120 songs within
    playlists
-   Quick restore: 1 second for every ~120 songs
-   Clean library: 1 second for every ~120 liked songs, 1 second for every 2-3
    playlists

## Backwards compatibility

If you have an old `backup.json`, rename it to `liked-songs.json` and place it
under a new directory, `backup`
