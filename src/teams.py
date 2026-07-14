from dataclasses import dataclass
from games import Game

LEAGUE_TEAMS = {
    "ATL": "East", "BOS": "East", "BKN": "East", "CHA": "East", "CHI": "East",
    "CLE": "East", "DAL": "West", "DEN": "West", "DET": "East", "GSW": "West",
    "HOU": "West", "IND": "East", "LAC": "West", "LAL": "West", "MEM": "West",
    "MIA": "East", "MIL": "East", "MIN": "West", "NOP": "West", "NYK": "East",
    "OKC": "West", "ORL": "East", "PHI": "East", "PHX": "West", "POR": "West",
    "SAC": "West", "SAS": "West", "TOR": "East", "UTA": "West", "WAS": "East",
}

@dataclass
class Team:
    """Represents a team in the league"""
    name: str
    conference: str
    wins: int
    losses: int
    win_pct: float


def compute_standings(games: list[Game]) -> list[Team]:
    """Calculates team stats for completed games in current season"""
    wins = {team: 0 for team in LEAGUE_TEAMS}
    losses = {team: 0 for team in LEAGUE_TEAMS}

    for game in games:
        if game.home_score > game.away_score:
            wins[game.home_team] += 1
            losses[game.away_team] += 1
        else:
            wins[game.away_team] += 1
            losses[game.home_team] += 1

    teams = []
    for team, conference in LEAGUE_TEAMS:
        win_pct = round(wins[team] / (wins[team] + losses[team]), 3)
        teams.append(Team(team, conference, wins[team], losses[team], win_pct))

    return teams