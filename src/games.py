import requests
import os
from dataclasses import dataclass
from datetime import date, datetime

API_KEY = os.getenv("BALLDONTLIE_API_KEY")
BASE_URL = "https://api.balldontlie.io/v1"
headers = {"Authorization": API_KEY}

@dataclass
class Game:
    """Represents a game on the schedule"""
    id: int
    datetime: datetime
    home_team: str
    away_team: str
    postseason: bool


def fetch_games(start: str, end: str) -> str:
    """Returns all games within specified time range"""
    if API_KEY is None:
        raise RuntimeError("No API Key")

    # start = date.today().isoformat() # change back after testing
    url = f"{BASE_URL}/games"
    response = requests.get(
        url,
        headers=headers,
        params={"per_page": 100, "start_date": start, "end_date": end}
    )

    games = response.json()
    return parse_all(games["data"])


def parse_all(games: dict) -> list[Game]:
    """Returns all JSON data into formatted games"""
    parsed = []
    for game in games:
        parsed.append(parse_game(game))

    return parsed


def parse_game(game: dict) -> Game:
    """Parses and formats JSON data on a specific game"""
    return Game(game["id"], datetime.fromisoformat(game["datetime"]).astimezone(),
                game["home_team"]["abbreviation"], game["visitor_team"]["abbreviation"],
                game["postseason"])