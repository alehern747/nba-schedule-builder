from games import Game
from teams import Team

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

    for team in teams.values():
        games_played = team.wins + team.losses
        if games_played == 0:
            team.win_pct = 0.0
        else:
            team.win_pct = round(team.wins / games_played, 3)

    return list(teams.values()), new_games