from enum import IntEnum
from collections import namedtuple
from datetime import datetime, timedelta
from games import Game
from scoring import calculate_score

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
    """Builds and scores multiple schedules matching user preferences."""
    def __init__(self, user, games, standings):
        self._user = user
        self._games = games
        self._standings = standings
        self._selected_games = []
        self._best_schedule = None

    @property
    def score(self) -> float:
        """Returns score of the current working schedule."""
        return calculate_score(self._user,
                               self._selected_games,
                               self._standings)

    @property
    def best_score(self) -> float:
        """Returns score of the best schedule constructed so far."""
        return calculate_score(self._user,
                               self._best_schedule,
                               self._standings) if self._best_schedule else 0.0

    def update_best(self):
        """Sets the current working schedule as the best schedule."""
        self._best_schedule = self._selected_games.copy()

    def add(self, index):
        """Adds a game to the current working schedule."""
        self._selected_games.append(self._games[index])

    def remove(self, index):
        """Removes a game from the current working schedule."""
        self._selected_games.remove(self._games[index])


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