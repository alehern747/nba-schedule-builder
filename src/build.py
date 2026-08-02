from datetime import time
from games import Game
from collections import namedtuple
from database import retrieve_standings

Timeframe = namedtuple("Timeframe", ["start", "end"])

# need to disallow overlapping timeframes, through UI
# needs to adapt to availabilities for different days (task scheduling dp)
# combine all filters, reduce to checking individual games?

def filter_availability(games: list[Game], *timeframes) -> list[Game]:
    """Filters out games outside of daily availability"""
    available_games = []

    for game in games:
        game_time = game.datetime.time()
        for timeframe in timeframes:
            if timeframe.start <= game_time <= timeframe.end:
                available_games.append(game)
                break

    return available_games

def filter_teams(games: list[Game], *teams) -> list[Game]:
    """Filters out games involving disliked teams"""
    filtered_games = []

    for game in games:
        if game.home_team not in teams and game.away_team not in teams:
            filtered_games.append(game)

    return filtered_games

def filter_favorite_teams(games: list[Game], *favorites) -> list[Game]:
    """Filters out all games without favorite teams playing"""
    filtered_games = []

    for game in games:
        if game.home_team in favorites or game.away_team in favorites:
            filtered_games.append(game)

    return filtered_games

def filter_below_win_pct(games: list[Game], db: str, threshold: float, adj_formula=None) -> list[Game]:
    """Filters out all games involving a team with a win % below given threshold %"""
    filtered_games = []
    teams = retrieve_standings(db)
    previous_teams = retrieve_standings(db, previous=True)

    if adj_formula:
        metric = adj_formula
    else:
        metric = lambda current, previous: current.win_pct

    for game in games:
        home_win_pct = metric(teams[game.home_team], previous_teams[game.home_team])
        away_win_pct = metric(teams[game.away_team], previous_teams[game.away_team])

        if home_win_pct >= threshold and away_win_pct >= threshold:
            filtered_games.append(game)

    return filtered_games


def filter_matchups(games: list[Game], db: str, max_diff: float, adj_formula=None) -> list[Game]:
    """Filters out all uncompetitive matchups (games between teams of high win_pct disparity)"""
    filtered_games = []
    teams = retrieve_standings(db)
    previous_teams = retrieve_standings(db, previous=True)

    if adj_formula:
        metric = adj_formula
    else:
        metric = lambda current, previous: current.win_pct

    for game in games:
        home_win_pct = metric(teams[game.home_team], previous_teams[game.home_team])
        away_win_pct = metric(teams[game.away_team], previous_teams[game.away_team])

        disparity = abs(home_win_pct - away_win_pct)
        if disparity <= max_diff:
            filtered_games.append(game)

    return filtered_games