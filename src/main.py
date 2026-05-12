from datetime import date
from games import fetch_games, parse_all

def format_datetime(year, month, day) -> str:
    """Formats and returns a valid date"""
    start_date = date(year, month, day)
    if start_date <= date.today():
        raise ValueError
    if start_date.year > date.today().year + 1:
        raise ValueError
    return start_date.isoformat()

if __name__ == "__main__":
    parse_all(fetch_games(format_datetime(2026, 5, 15)))