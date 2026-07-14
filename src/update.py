from games import fetch_games
from teams import Team, LEAGUE_TEAMS
import sqlite3

def refresh():
    # here, we should fetch games incrementally, eventually
    completed = [g for g in fetch_games(format_datetime(2025, 8, 21), format_datetime(2025, 8, 30)) if g.status == "Final"]
    save_standings(compute_standings(completed))
