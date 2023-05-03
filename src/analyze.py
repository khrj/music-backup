from json import load
from io import BytesIO
from pathlib import Path
from statistics import mean, median, mode, variance, stdev

from pygal import Pie
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from backup import slugify


def analyze(file_path):
    raw_data = load(open(file_path, "r"))
    name = raw_data["name"] if "tracks" in raw_data else "Liked Songs"
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

    print(f"{name}:")
    print(by_decade)
    print()
    print(f"Mean: {mean(tracks)}")
    print(f"Median: {median(tracks)}")
    print(f"Mode: {mode(tracks)}")
    print(f"Variance: {variance(tracks)}")
    print(f"Standard Deviation: {stdev(tracks)}")
    print()
    print()
    print()

    pie_chart = Pie(print_values=True)
    pie_chart.title = f'Decade distribution for "{name}" [Average: {mean(tracks):.2f}]'

    for year, count in by_decade.items():
        pie_chart.add(year, count)

    Path("outputs").mkdir(parents=True, exist_ok=True)
    renderPM.drawToFile(
        svg2rlg(BytesIO(pie_chart.render())), f"outputs/{slugify(name)}.png", fmt="PNG"
    )
