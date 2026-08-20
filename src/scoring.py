from games import Game
from teams import RIVALRIES
from standings import get_game_win_pcts

# Scoring weights (must add up to 100)
FAVORITE_WEIGHT = 50.0
TEAM_QUALITY_WEIGHT = 20.0
RIVALRY_WEIGHT = 15.0
MATCHUP_WEIGHT = 15.0

def calculate_score(user: 'User', schedule: list[Game], standings) -> float:
    """Calculate schedule scores as tiebreakers using personal and universal game preferences.
    All game weights add up to 100 points."""
    score = 0.0

    for game in schedule:
        score += (_favorite_score(game, user) * FAVORITE_WEIGHT)

        if _is_rivalry(game):
            score += RIVALRY_WEIGHT

        home_win_pct, away_win_pct = get_game_win_pcts(game, standings, user.win_pct_metric)

        team_quality = (home_win_pct + away_win_pct) / 2
        score += team_quality * TEAM_QUALITY_WEIGHT

        matchup_quality = 1 - abs(home_win_pct - away_win_pct)
        score += matchup_quality * MATCHUP_WEIGHT

        # calculate win streak (unfinished)

    return score

def _favorite_score(game: Game, user: 'User') -> float:
    """Returns a 0-1 score based on favorite team preference."""
    for index, team in enumerate(user.favorite_teams, start = 1):
        if game.home_team == team or game.away_team == team:
            return 1 / index

    return 0.0

def _is_rivalry(game: Game) -> bool:
    """Returns whether the game includes a known rivalry."""
    return (
        (game.home_team, game.away_team) in RIVALRIES
        or (game.away_team, game.home_team) in RIVALRIES
    )