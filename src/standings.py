from games import Game
from database import retrieve_processed_games, retrieve_standings, save_games
from teams import Team

def compute_standings(games: list[Game]) -> list[Team]:
    """Calculates team stats for completed games in current season"""
    teams = retrieve_standings()
    processed = retrieve_processed_games()
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

    save_games(new_games)

    for team in teams.values():
        games_played = team.wins + team.losses
        if games_played == 0:
            team.win_pct = 0.0
        else:
            team.win_pct = round(team.wins / games_played, 3)

    return list(teams.values())