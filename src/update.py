from games import fetch_games
from teams import Team, LEAGUE_TEAMS
import sqlite3

def refresh():
    # here, we should fetch games incrementally, eventually
    completed = [g for g in fetch_games(format_datetime(2025, 8, 21), format_datetime(2025, 8, 30)) if g.status == "Final"]
    save_standings(compute_standings(completed))


def create_database():
    """Initializes a SQL database containing relevant stats on games and teams"""
    with sqlite3.connect("nba.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS STANDINGS (
                team VARCHAR PRIMARY KEY,
                conference VARCHAR,
                wins INTEGER,
                losses INTEGER,
                win_pct REAL)
            """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS PROCESSED_GAMES (
                game_id INTEGER PRIMARY KEY
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS METADATA (
                key VARCHAR PRIMARY KEY,
                value VARCHAR
            )
        """)

        conn.close()


if __name__ == "__main__":
    create_database()