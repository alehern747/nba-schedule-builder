from dataclasses import dataclass

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

    @property
    def win_pct(self) -> float:
        games_played = self.wins + self.losses
        return self.wins / games_played if games_played else 0.0