from client import get_all_pages, parse_all
from dataclasses import dataclass
from datetime import date, datetime

@dataclass
class Game:
    """Represents a game on the schedule"""
    id: int
    datetime: datetime
    home_team: str
    away_team: str
    home_score: int
    away_score: int
    status: str
    postseason: bool

def fetch_games(start: str, end: str) -> list[Game]:
    """Returns all games within specified time range"""
    games = get_all_pages("games", {"per_page": 100, "start_date": start, "end_date": end})
    return parse_all(games, parse_game)

def parse_game(game: dict) -> Game:
    """Parses and formats JSON data on a specific game"""
    return Game(game["id"],
                datetime.fromisoformat(game["datetime"]).astimezone(),
                game["home_team"]["abbreviation"],
                game["visitor_team"]["abbreviation"],
                game["home_team_score"],
                game["visitor_team_score"],
                game["status"],
                game["postseason"])