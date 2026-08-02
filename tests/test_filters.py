import unittest
import datetime
import os
from src.games import Game
from src.teams import Team
from src.build import (Timeframe, filter_availability, filter_favorite_teams, filter_teams,
                       filter_below_win_pct, filter_matchups)
from test_data import TEST_GAMES, TEST_TEAMS, TEST_PREVIOUS_SEASON
from src.database import create_database, save_standings
from src.standings import bayesian_shrinkage

class FilterGameTest(unittest.TestCase):
    def setUp(self):
        self.db = "test.db"
        self.test_games = list(TEST_GAMES)
        create_database(self.db)
        save_standings(self.db, TEST_TEAMS)
        save_standings(self.db, TEST_PREVIOUS_SEASON, previous=True)

    def tearDown(self):
        os.remove(self.db)

    def test_empty_game_list_returns_empty(self):
        self.assertEqual(filter_below_win_pct([], self.db, 0.5),[])

    def test_all_games_within_daily_timeframe_retrieved(self):
        timeframe = Timeframe(datetime.time(12), datetime.time(17))
        filtered = filter_availability(self.test_games, timeframe)
        expected = self.test_games
        for i in [13, 12, 11, 3, 1]:
            expected.pop(i)
        self.assertEqual(filtered, expected)

    def test_all_games_excluding_disliked_teams_retrieved(self):
        filtered = filter_teams(self.test_games, 'LAL', 'CLE')
        expected = self.test_games
        expected.pop(2)
        expected.pop(1)
        self.assertEqual(filtered, expected)

    def test_filter_teams_with_no_disliked_returns_all_games(self):
        filtered = filter_teams(self.test_games)
        self.assertEqual(filtered, self.test_games)

    def test_all_games_including_favorite_team_retrieved(self):
        filtered = filter_favorite_teams(self.test_games, 'LAL')
        self.assertEqual(filtered, [self.test_games[1]])

    def test_filter_favorite_unknown_team_returns_empty(self):
        filtered = filter_favorite_teams(self.test_games,"XYZ")
        self.assertEqual(filtered, [])

    def test_all_games_above_win_pct_retrieved(self):
        filtered = filter_below_win_pct(self.test_games, self.db, 0.5)
        expected = self.test_games
        for i in [12, 11, 10, 9, 7, 5, 4, 3]:
            expected.pop(i)
        self.assertEqual(filtered, expected)

    def test_zero_win_pct_threshold_returns_all_games(self):
        filtered = filter_below_win_pct(self.test_games, self.db,0.0)
        self.assertEqual(filtered, self.test_games.copy())

    def test_all_even_matchups_retrieved(self):
        filtered = filter_matchups(self.test_games, self.db, 0.25)
        expected = self.test_games
        for i in [10, 7, 4, 3, 0]:
            expected.pop(i)
        self.assertEqual(filtered, expected)

    def test_large_matchup_threshold_returns_all_games(self):
        filtered = filter_matchups(self.test_games, self.db,1.0)
        self.assertEqual(filtered, self.test_games)

    def test_bayesian_shrinkage_formula_returns_correct_value(self):
        current_team = Team("ATL", "EAST", 7, 2)
        previous_team = Team("ATL", "EAST", 40, 42)
        self.assertAlmostEqual(bayesian_shrinkage(current_team, previous_team), 0.57779647, delta=0.0001)

    def test_matchups_accepts_metric(self):
        def metric(current, previous):
            return 1.0

        filtered = filter_matchups(self.test_games, self.db, 0.5, metric)
        self.assertEqual(filtered, self.test_games)

    def test_below_win_pct_accepts_metric(self):
        def metric(current, previous):
            return 1.0

        filtered = filter_below_win_pct(self.test_games, self.db, 0.5, metric)
        self.assertEqual(filtered, self.test_games)

    def test_all_games_above_adjusted_win_pct_retrieved(self):
        filtered = filter_below_win_pct(self.test_games, self.db, 0.5, bayesian_shrinkage)
        expected = []
        for i in [0, 1, 2, 8]:
            expected.append(self.test_games[i])
        self.assertEqual(filtered, expected)

    def test_all_even_matchups_with_adjusted_win_pct_retrieved(self):
        filtered = filter_matchups(self.test_games, self.db, 0.20, bayesian_shrinkage)
        expected = self.test_games
        for i in [11, 10, 9, 7, 0]:
            expected.pop(i)
        self.assertEqual(filtered, expected)


if __name__ == '__main__':
    unittest.main()
