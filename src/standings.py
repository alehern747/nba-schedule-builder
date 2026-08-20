from games import Game
from teams import Team
from database import retrieve_standings, save_standings, delete_season
from dataclasses import dataclass

DEFAULT_PRIOR_GAMES = 20

@dataclass
class StandingsContext:
    current: dict
    previous: dict

def get_standings_context(db: str) -> StandingsContext:
    """Returns current and previous team standings together"""
    return StandingsContext(current=retrieve_standings(db),
                            previous=retrieve_standings(db, previous=True))

def get_game_win_pcts(game: Game, standings: StandingsContext, metric=None) -> tuple[float, float]:
    """Calculates win % of two teams participating in a game using metric, if any."""
    if metric:
        formula = metric
    else:
        formula = lambda current, previous: current.win_pct

    home_win_pct = formula(standings.current[game.home_team], standings.previous[game.home_team])
    away_win_pct = formula(standings.current[game.away_team], standings.previous[game.away_team])

    return home_win_pct, away_win_pct


def compute_standings(games: list[Game], teams: dict[str, Team], processed: list[int]) -> list[Team]:
    """Calculates team stats for completed games in current season"""
    new_games = []

    for game in games:
        if game.id in processed:
            continue

        new_games.append(game.id)

        if game.home_score > game.away_score:
            teams[game.home_team].wins += 1
            teams[game.away_team].losses += 1
        else:
            teams[game.away_team].wins += 1
            teams[game.home_team].losses += 1

    return list(teams.values()), new_games

# Formulas for win_pct calculation
def bayesian_shrinkage(team: Team, previous: Team):
    """Re-evaluates current season win % based on number of games played and previous
    season standings for small early season sample size"""
    return ((team.wins + previous.win_pct * DEFAULT_PRIOR_GAMES)
            / (team.wins + team.losses + DEFAULT_PRIOR_GAMES))