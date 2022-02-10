# Spotify backup

Backup spotify liked songs to transfer them to a different account

Features:

* Keeps order of liked songs

> Note: Until spotify approves an application for this app's client ID,
> you will have to use your own client ID, which you can generate by going
> to https://developer.spotify.com/dashboard/applications and then substitute
> into the beginning of the appropriate script

## Backup

Run

```bash
python scripts/backup.py
```

## Restore

**Time taken:** 1 second per song

Run

```bash
python scripts/restore.py
```

## Quick restore

**Note: This will not preserve the order of backed up liked songs**  
**Time taken:** Nearly instantaneous

Run

```bash
python scripts/quick_restore.py
```

## Clean library

Run

```bash
python scripts/clean_library.py
```