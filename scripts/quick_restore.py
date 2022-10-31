from json import load


def quick_restore(sp):
    backup = load(open("backup/liked-songs.json", "r"))

    ids = [item["id"] for item in reversed(backup)]
    batches = [ids[i : i + 50] for i in range(0, len(ids), 50)]

    for batch in batches:
        sp.current_user_saved_tracks_add(batch)
