from games import fetch_games
from standings import compute_standings
from database import retrieve_last_refresh, save_standings, delete_season
from client import format_datetime

def refresh():
    """Daily refresh of SQL database, including team data and relevant metadata"""
    #last_refresh = retrieve_last_refresh()
    #if not last_refresh:
        # start of NBA season, auto update by year

    # keep variable for testing purposes, later set auto increment time to 1 day buffer overlap
    last_refresh = format_datetime(2025, 10, 29)

    completed = [g for g in fetch_games(last_refresh, format_datetime(2025, 11, 4)) if g.status == "Final"]
    save_standings(compute_standings(completed))

# Update to smaller reset later, only up to certain time range?
def reset():
    """Deletes all data in the database."""
    delete_season()
