from json import load

before_raw = load(open("backup/liked-songs.json", "r"))
after_raw = load(
    open("backup/playlists/followed/<playlistnamehere>.json", "r")
)

if "tracks" in before_raw:
    before_raw = before_raw["tracks"]

if "tracks" in after_raw:
    after_raw = after_raw["tracks"]


before_tracks = set([x["name"] for x in before_raw])
after_tracks = set([x["name"] for x in after_raw])

common = before_tracks.intersection(after_tracks)

print(f"{len(common)} tracks common ({len(before_tracks)} ⇔ {len(after_tracks)}):")
print("===========================")
print()

for i, track in enumerate(common):
    print(f"{i + 1}. {track}")
