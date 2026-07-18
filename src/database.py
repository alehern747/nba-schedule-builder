import sqlite3
from teams import Team, LEAGUE_TEAMS
from datetime import datetime

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

    update_last_refresh()


def save_games(game_ids: list[str]):
    """Saves IDs of newly added games to the database, to avoid recounting."""
    with sqlite3.connect("nba.db") as conn:
        cursor = conn.cursor()
        cursor.executemany("""
            INSERT INTO PROCESSED_GAMES (game_id)
            VALUES (?) 
        """, [(id,) for id in game_ids])


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
        """, ("last_refresh", current_time))


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

        if row is None:
            return None
        else:
            return row[0]


def retrieve_standings() -> dict[str, list[Team]]:
    """Returns formatted standings for all teams from the database. If no existing data,
    returns empty standings"""
    with sqlite3.connect("nba.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT team, conference, wins, losses
            FROM STANDINGS
        """)

        rows = cursor.fetchall()

        teams = {}
        if not rows:
            for team, conference in LEAGUE_TEAMS.items():
                teams[team] = Team(team, conference, 0, 0, 0.0)
        else:
            for row in rows:
                teams[row[0]] = Team(row[0], row[1], row[2], row[3], 0.0)

        return teams


def retrieve_processed_games():
    """Returns all games already accounted for in database"""
    with sqlite3.connect("nba.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT game_id
            FROM PROCESSED_GAMES
        """)

        processed = {row[0] for row in cursor.fetchall()}
        return processed


def delete_season():
    """Deletes all seasonal data in the database"""
    with sqlite3.connect("nba.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM STANDINGS")
        cursor.execute("DELETE FROM PROCESSED_GAMES")
        cursor.execute("DELETE FROM METADATA")