from datetime import time
from games import Game
from collections import namedtuple

Timeframe = namedtuple("Timeframe", ["start", "end"])

# need to disallow overlapping timeframes, through UI
# needs to adapt to availabilities for different days (task scheduling dp)
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

# combine all filters, reduce to checking individual games?
def filter_teams(games: list[Game], *teams) -> list[Game]:
    """Filters out games involving disliked teams"""
    filtered_games = []

    for game in games:
        if game.home_team not in teams and game.away_team not in teams:
            filtered_games.append(game)

    return filtered_games