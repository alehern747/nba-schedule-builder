from enum import IntEnum
from collections import namedtuple
from datetime import datetime, timedelta
from games import Game

Timeframe = namedtuple("Timeframe", ["start", "end"])

class Weekday(IntEnum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

class Scheduler:
    pass

def matching_timeframe(game: Game, schedule: dict[Weekday, list[Timeframe]], min_watch_time: timedelta) -> Timeframe | None:
    """Finds available user timeframe for a game, if any."""
    game_time = game.datetime.time()
    game_day = Weekday(game.datetime.weekday())
    watch_end = (game.datetime + min_watch_time).time()

    for timeframe in schedule[game_day]:
        if timeframe.start <= game_time <= timeframe.end and timeframe.start <= watch_end <= timeframe.end:
            return timeframe

    return None

def filter_availability(games: list[Game], schedule: dict[Weekday, Timeframe], min_watch_time: timedelta) -> list[Game]:
    """Filters out games outside of daily availability"""
    available_games = []

    for game in games:
        if matching_timeframe(game, schedule, min_watch_time):
            available_games.append(game)

    return available_games