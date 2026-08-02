import unittest
import datetime
import os
from src.games import Game
from src.build import (Timeframe, filter_availability, filter_favorite_teams, filter_teams,
                       filter_below_win_pct, filter_matchups)
from test_data import TEST_GAMES, TEST_TEAMS
from database import create_database, save_standings

class FilterGameTest(unittest.TestCase):
    def setUp(self):
        self.db = "test.db"
        self.test_games = list(TEST_GAMES)
        create_database(self.db)
        save_standings(self.db, TEST_TEAMS)

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
        self.assertEqual(filtered, self.test_games)

    def test_all_even_matchups_retrieved(self):
        filtered = filter_matchups(self.test_games, self.db, 0.25)
        expected = self.test_games
        for i in [10, 7, 4, 3, 0]:
            expected.pop(i)
        self.assertEqual(filtered, expected)

    def test_large_matchup_threshold_returns_all_games(self):
        filtered = filter_matchups(self.test_games, self.db,1.0)
        self.assertEqual(filtered, self.test_games)


    # more tests
        # multiple favorite teams
        # returning an empty list
        # multiple timeframes
        # day-specific timeframes

if __name__ == '__main__':
    unittest.main()
