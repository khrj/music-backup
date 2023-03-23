# Spotify backup

Backup spotify liked songs and playlists to transfer them to a different account

Features:

-   Backs up liked songs
    -   Keeps order of liked songs
-   Backs up albums
-   Backs up playlists (followed, collaborative and created)
    -   Re-follows playlists on restore
    -   Recreates collaborative and created playlists
-   Backs up followed artists
-   Backs up list of people in your blends
    - CAVEAT: Blends with more than a ceratin amount of people will only have "X others" instead of all member names
- **Maintains a git repository of your songs at backup/. Can optionally push to a remote**

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

To automatically backup (in a script, on a schedule...):

```bash
poetry run python src/main.py --backup
```

## Time taken

> **Quick restore causes liked songs to lose order. Playlists are always ordered
> correctly.**

(Times given are estimates)

| Operation     | Liked Songs | Playlists       | Albums       | Arists        |
| ------------- | ----------- | --------------- | ------------ | ------------- |
| Backup        | 120 songs/s | 120 songs/s     | 120 albums/s | 120 artists/s |
| Restore       | 1 song/s    | 120 songs/s     | 120 albums/s | 120 artists/s |
| Quick Restore | 120 songs/s | 120 songs/s     | 120 albums/s | 120 artists/s |
| Clean Library | 120 songs/s | 2.5 playlists/s | 120 albums/s | 120 artists/s |

The total time taken to perform any of these operations is the sum of each type
of item in your library divided by its respective speed

## Backwards compatibility

If you have an old `backup.json`, rename it to `liked-songs.json` and place it
under a new directory, `backup`
