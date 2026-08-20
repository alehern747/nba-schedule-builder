from enum import IntEnum
from collections import namedtuple
from datetime import datetime, timedelta
from games import Game
from scoring import calculate_score
from collections import defaultdict

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
    """Builds the highest-scoring schedule matching user preferences."""
    def __init__(self, user, games, standings):
        self._user = user
        self._games = games
        self._standings = standings

    def build(self) -> list[Game]:
        """Return the highest-scoring valid schedule."""
        games_by_day = self._group_games_by_day()

        schedule = []

        for games in games_by_day.values():
            schedule.extend(self._optimize_day(games))

        return sorted(schedule, key=lambda game: game.datetime) # does it need to be sorted?

    def _group_games_by_day(self) -> dict:
        """Group candidate games by calendar day."""
        games_by_day = defaultdict(list)

        for game in self._games:
            games_by_day[game.datetime.date()].append(game)

        return games_by_day

    def _optimize_day(self, games: list[Game]) -> list[Game]:
        """Return the highest-scoring valid selection for one day."""
        scored_games = [(game,
                         calculate_game_score(self._user, game, self._standings))
                        for game in games]

        scored_games.sort(key = lambda item: item[1], reverse = True)

        best_schedule = []
        best_score = 0.0
        selected = []

        def backtrack(i: int, current_score: float) -> None:
            nonlocal best_schedule, best_score

            if current_score > best_score:
                best_score = current_score
                best_schedule = selected.copy()

            if i == len(scored_games):
                return

            if len(selected) >= self._user.daily_max_games:
                return

            game, game_score = scored_games[i]

            if self._can_add(game, selected):
                selected.append(game)
                backtrack(i + 1, current_score + game_score)
                selected.pop()

            backtrack(i + 1, current_score)

        backtrack(0, 0.0)

        return best_schedule

    def _can_add(self, candidate: Game, selected: list[Game]) -> bool:
        """Return whether candidate respects simultaneous-game capacity."""
        games = selected + [candidate]

        for game in games:
            start = game.datetime

            simultaneous = sum(
                other.datetime <= start
                < (other.datetime + self._user.min_watch_time)
                for other in games
            )

            if simultaneous > self._user.max_simultaneous_games:
                return False

        return True

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