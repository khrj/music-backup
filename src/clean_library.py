from backup import get_followed_artists, get_liked_songs, get_playlists, get_albums


def clean_library(sp):
    liked_songs = get_liked_songs(sp)
    ids = [item["id"] for item in liked_songs]
    batches = [ids[i : i + 50] for i in range(0, len(ids), 50)]
    for batch in batches:
        sp.current_user_saved_tracks_delete(batch)

    albums = get_albums(sp)
    ids = [item["id"] for item in albums]
    batches = [ids[i : i + 50] for i in range(0, len(ids), 50)]
    for batch in batches:
        sp.current_user_saved_albums_delete(batch)

    playlists = get_playlists(sp)
    for playlist in playlists:
        sp.current_user_unfollow_playlist(playlist["id"])

    followed = get_followed_artists(sp)
    ids = [item["id"] for item in followed]
    batches = [ids[i : i + 50] for i in range(0, len(ids), 50)]
    for batch in batches:
        sp.user_unfollow_artists(batch)
