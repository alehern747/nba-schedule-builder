from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Callable

from schedule import Weekday, Timeframe

@dataclass
class User:
    daily_max_games: int
    min_win_pct: float
    win_pct_diff: float
    min_watch_time: timedelta
    favorite_teams: list[str] # change to sets later?
    blocked_teams: list[str]
    schedule: dict[Weekday, list[Timeframe]]
    simultaneous: bool
    win_pct_metric: Callable