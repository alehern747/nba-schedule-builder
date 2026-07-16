from games import fetch_games
from teams import Team, LEAGUE_TEAMS
import sqlite3
from datetime import datetime

def refresh():
    # here, we should fetch games incrementally, eventually
    # 1st datetime: date of last refresh, - a couple of days for overlap
    # 2nd datetime: the date we want to sim to, should be current day in final sim

    last_refresh = retrieve_last_refresh()
    if not last_refresh:
        last_refresh = format_datetime(2025, 8, 21) # start of NBA season

    completed = [g for g in fetch_games(last_refresh, format_datetime(2025, 8, 30)) if g.status == "Final"]
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


def save_standings(teams: list[Team]):
    """Updates team database with most recent win / loss data for the current season"""
    with sqlite3.connect("nba.db") as conn:
        cursor = conn.cursor()

        for team in teams:
            cursor.execute("""
                INSERT INTO STANDINGS (
                    team,
                    conference,
                    wins,
                    losses,
                    win_pct
                )
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(team) DO UPDATE SET
                    conference = excluded.conference,
                    wins = excluded.wins,
                    losses = excluded.losses,
                    win_pct = excluded.win_pct
            """, (
                team.name,
                team.conference,
                team.wins,
                team.losses,
                team.win_pct
            ))
        conn.close()

    update_last_refresh()


def update_last_refresh():
    """Logs the date and time of the last update to the team database"""
    with sqlite3.connect("nba.db") as conn:
        cursor = conn.cursor()
        current_time = datetime.now().isoformat(timespec='minutes')

        cursor.execute("""
            INSERT INTO METADATA (key, value)
            VALUES (?, ?)
            ON CONFLICT (key) DO UPDATE SET
                value = excluded.value
        """), ("last_refresh", current_time)

        conn.close()


def retrieve_last_refresh():
    """Returns last time team database was updated, if ever"""
    with sqlite3.connect("nba.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT value
            FROM METADATA
            WHERE key = ?
        """, ("last_refresh",))

        row = cursor.fetchone()
        conn.close()

        if row is None:
            return None
        else:
            return row[0]


if __name__ == "__main__":
    # create_database()
    pass