from games import fetch_games
from standings import compute_standings
from database import retrieve_last_refresh, save_standings
from main import format_datetime

def refresh():
    """Daily refresh of SQL database, including team data and relevant metadata"""
    last_refresh = retrieve_last_refresh()
    if not last_refresh:
        last_refresh = format_datetime(2025, 8, 21) # start of NBA season, auto update by year

    completed = [g for g in fetch_games(last_refresh, format_datetime(2025, 8, 30)) if g.status == "Final"]
    save_standings(compute_standings(completed))


if __name__ == "__main__":
    # create_database()
    # refresh()
    pass