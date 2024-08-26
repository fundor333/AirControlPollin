import os
import requests
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown

GOOGLETOKEN = os.environ["GOOGLETOKEN"]

LAT = 45.437984
LONG = 12.335898

LANGUAGE = "it"
DAYS = 1

AIR_QUALITY = f"https://airquality.googleapis.com/v1/currentConditions:lookup?key={GOOGLETOKEN}"
POLLEN = f"https://pollen.googleapis.com/v1/forecast:lookup?key={GOOGLETOKEN}"

POLLEN_INDEX = [
    "😊😊😊😊😊",
    "😊😊😊😊☠️",
    "😊😊😊☠️☠️",
    "😊😊☠️☠️☠️",
    "😊☠️☠️☠️☠️",
    "☠️☠️☠️☠️☠️",
]

console = Console()


def iqa_color(code: int) -> str:
    if code > 79:
        return "#009E3A"
    elif code > 59:
        return "#84CF33"
    elif code > 39:
        return "#FFFF00"
    elif code > 19:
        return "#FF8C00"
    elif code > 0:
        return "#FF0000"
    return "#800000"


def get_air():
    console.print(Markdown("# AIR QUALITY"))
    r = requests.post(
        AIR_QUALITY,
        json={
            "location": {"latitude": LAT, "longitude": LONG},
            "extraComputations": [
                "HEALTH_RECOMMENDATIONS",
            ],
            "universalAqi": True,
            "languageCode": LANGUAGE,
        },
    )

    data = r.json()
    for e in data["indexes"]:
        console.print(
            Markdown("## " + e["category"]), style=iqa_color(e["aqi"])
        )

    table = Table(show_lines=True)
    table.add_column("Category", justify="right", no_wrap=True)
    table.add_column("Recommendation")

    for a, b in data["healthRecommendations"].items():
        table.add_row(a, b)
    console.print(table)


def get_pollen():
    r = requests.get(
        POLLEN,
        params={
            "location.longitude": LONG,
            "location.latitude": LAT,
            "languageCode": LANGUAGE,
            "days": DAYS,
            "plantsDescription": False,
        },
    )

    data = r.json()
    for e in data["dailyInfo"]:
        datas = e["date"]
        console.print(
            Markdown(f"## {datas['year']}/{datas['month']}/{datas['day']}")
        )

        table = Table(show_lines=True)
        table.add_column("Display Name", justify="right", no_wrap=True)
        table.add_column("Level")
        table.add_column("")

        for element in e["plantInfo"]:
            if element.get("indexInfo", False):
                table.add_row(
                    element["displayName"],
                    POLLEN_INDEX[element["indexInfo"]["value"]],
                    element["indexInfo"]["indexDescription"],
                )
        console.print(table)
