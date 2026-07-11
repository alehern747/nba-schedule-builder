import datetime
from datetime import date
from games import fetch_games
from build import Timeframe, filter_availability, filter_teams, filter_favorite_teams

def format_datetime(year, month, day) -> str:
    """Formats and returns a valid date"""
    formatted = date(year, month, day)
    # remove comment after testing previous date
    # if start_date <= date.today():
        # raise ValueError
    # if start_date.year > date.today().year + 1:
        # raise ValueError
    return formatted.isoformat()

if __name__ == "__main__":
    print(fetch_games(format_datetime(2025, 10, 21), format_datetime(2025, 10, 22)))