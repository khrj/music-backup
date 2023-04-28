from json import load


def analyze(file_path):
    raw_data = load(open(file_path, "r"))
    if "tracks" in raw_data:
        raw_data = raw_data["tracks"]

    tracks = sorted(
        [
            int(x["release_date"].split("-")[0])
            for x in raw_data
            if x["release_date"] != "0000"
        ]
    )

    by_decade = {}

    for t in tracks:
        decade = str(t)[:-1] + "0s"
        if decade in by_decade:
            by_decade[decade] = by_decade[decade] + 1
        else:
            by_decade[decade] = 1

        if decade == "0s":
            print(t)

    print(by_decade)


# import matplotlib.pyplot as plt
# plt.pie(data.values(), labels=data.keys())
# plt.show()
