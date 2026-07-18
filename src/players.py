from dataclasses import dataclass
from collections import namedtuple
from client import get_all_pages

Player = namedtuple("Player", ["name", "team"])

# Revisit when designing player search, accompanying UI
def fetch_player_teams(player_ids: list[int]) -> list[Player]:
    """Returns teams of all players matching IDs."""
    players = get_all_pages("players", {"per_page": 100, "player_ids": player_ids})
    return {player["team"]["abbreviation"] for player in players}