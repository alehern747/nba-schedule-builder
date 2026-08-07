import unittest
import datetime
from datetime import timedelta, time
import os
from src.games import Game
from src.teams import Team
from src.filter import filter_favorite_teams, filter_teams, filter_below_win_pct, filter_matchups
from src.schedule import filter_availability, Timeframe, Weekday
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

        self.schedule = {day: [] for day in Weekday}

    def tearDown(self):
        os.remove(self.db)

    def test_empty_game_list_returns_empty(self):
        self.assertEqual(filter_below_win_pct([], self.db, 0.5),[])

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

    def test_game_that_fits_timeframe_is_returned(self):
        self.schedule[Weekday.TUESDAY] = [
            Timeframe(time(16, 0), time(18, 0))
        ]

        filtered = filter_availability(
            self.test_games,
            self.schedule,
            timedelta(hours=1),
        )

        self.assertEqual(filtered, [self.test_games[0]])

    def test_game_that_starts_before_timeframe_is_excluded(self):
        self.schedule[Weekday.TUESDAY] = [
            Timeframe(time(17, 0), time(19, 0))
        ]

        filtered = filter_availability(
            [self.test_games[0]],
            self.schedule,
            timedelta(hours=1),
        )

        self.assertEqual(filtered, [])

    def test_game_that_ends_after_timeframe_is_excluded(self):
        self.schedule[Weekday.TUESDAY] = [
            Timeframe(time(18, 0), time(19, 30))
        ]

        filtered = filter_availability(
            [self.test_games[1]],
            self.schedule,
            timedelta(hours=1),
        )

        self.assertEqual(filtered, [])

    def test_game_ending_exactly_at_timeframe_end_is_included(self):
        self.schedule[Weekday.TUESDAY] = [
            Timeframe(time(18, 0), time(20, 0))
        ]

        filtered = filter_availability(
            [self.test_games[1]],
            self.schedule,
            timedelta(hours=1),
        )

        self.assertEqual(filtered, [self.test_games[1]])

    def test_game_starting_exactly_at_timeframe_start_is_included(self):
        self.schedule[Weekday.WEDNESDAY] = [
            Timeframe(time(16, 0), time(18, 0))
        ]

        filtered = filter_availability(
            [self.test_games[2]],
            self.schedule,
            timedelta(hours=1),
        )

        self.assertEqual(filtered, [self.test_games[2]])

    def test_game_on_day_without_availability_is_excluded(self):
        self.schedule[Weekday.WEDNESDAY] = [
            Timeframe(time(16, 0), time(20, 0))
        ]

        filtered = filter_availability(
            [self.test_games[0]],
            self.schedule,
            timedelta(hours=1),
        )

        self.assertEqual(filtered, [])

    def test_multiple_games_can_fit_same_timeframe(self):
        self.schedule[Weekday.WEDNESDAY] = [
            Timeframe(time(15, 0), time(18, 0))
        ]

        games = [
            self.test_games[2],  # NYK @ CLE
            self.test_games[4],  # CHA @ BKN
            self.test_games[5],  # ORL @ MIA
            self.test_games[7],  # BOS @ PHI
        ]

        filtered = filter_availability(
            games,
            self.schedule,
            timedelta(hours=1),
        )

        self.assertEqual(filtered, games)

    def test_mixed_available_and_unavailable_games(self):
        self.schedule[Weekday.WEDNESDAY] = [
            Timeframe(time(16, 0), time(18, 0))
        ]

        games = [
            self.test_games[2],  # 16:00 — available
            self.test_games[3],  # 18:30 — unavailable
            self.test_games[7],  # 16:30 — available
            self.test_games[11], # 18:00 — available
        ]

        filtered = filter_availability(
            games,
            self.schedule,
            timedelta(hours=1),
        )

        self.assertEqual(
            filtered,
            [
                self.test_games[2],
                self.test_games[7],
            ],
        )

    def test_minimum_watch_time_determines_availability(self):
        game = self.test_games[1]

        self.schedule[Weekday.TUESDAY] = [
            Timeframe(time(18, 0), time(20, 0))
        ]

        self.assertEqual(
            filter_availability(
                [game],
                self.schedule,
                timedelta(hours=1),
            ),
            [game],
        )

        self.assertEqual(
            filter_availability(
                [game],
                self.schedule,
                timedelta(hours=1, minutes=1),
            ),
            [],
        )

if __name__ == '__main__':
    unittest.main()
