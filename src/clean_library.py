from backup import get_liked_songs


def clean_library(sp):
    liked_songs = get_liked_songs(sp)

    ids = [item["id"] for item in liked_songs]
    batches = [ids[i : i + 50] for i in range(0, len(ids), 50)]

    for batch in batches:
        sp.current_user_saved_tracks_delete(batch)
