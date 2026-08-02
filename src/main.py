from games import fetch_games
from build import Timeframe, filter_availability, filter_teams, filter_favorite_teams
from update import refresh
from client import format_datetime
from database import create_database


if __name__ == "__main__":
    create_database("nba.db")
    # refresh("nba.db")
    # print(fetch_games(format_datetime(2025, 10, 21), format_datetime(2025, 10, 22)))