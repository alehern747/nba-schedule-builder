import unittest
import datetime
from src.games import Game
from src.build import filter_availability, filter_favorite_teams, filter_teams, Timeframe
from test_data import TEST_GAMES

class FilterGameTest(unittest.TestCase):
    def setUp(self):
        self.test_games = list(TEST_GAMES)

    # THESE TESTS ARE BROKEN, GENERATE NEW DATA FOR TEST_GAMES
    def test_all_games_within_daily_timeframe_retrieved(self):
        timeframe = Timeframe(datetime.time(12), datetime.time(17))
        filtered = filter_availability(self.test_games, timeframe)
        expected = self.test_games
        expected.pop(13)
        expected.pop(12)
        expected.pop(11)
        expected.pop(3)
        expected.pop(1)
        self.assertEqual(filtered, expected)

    def test_all_games_excluding_disliked_teams_retrieved(self):
        filtered = filter_teams(self.test_games, 'LAL', 'CLE')
        expected = self.test_games
        expected.pop(2)
        expected.pop(1)
        self.assertEqual(filtered, expected)

    def test_all_games_including_favorite_team_retrieved(self):
        filtered = filter_favorite_teams(self.test_games, 'LAL')
        self.assertEqual(filtered, [self.test_games[1]])

    # more tests
        # multiple favorite teams
        # returning an empty list
        # multiple timeframes
        # day-specific timeframes

if __name__ == '__main__':
    unittest.main()
