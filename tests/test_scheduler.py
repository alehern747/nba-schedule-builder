import unittest
import os
from schedule import Scheduler, Weekday
from test_data import TEST_GAMES, TEST_PREVIOUS_SEASON, TEST_TEAMS
from user import User
from standings import bayesian_shrinkage, get_standings_context
from datetime import timedelta
from database import create_database, save_standings

class ScheduleGameTest(unittest.TestCase):
    def setUp(self):
        self.db = "test.db"
        self.test_games = list(TEST_GAMES)
        create_database(self.db)
        save_standings(self.db, TEST_TEAMS)
        save_standings(self.db, TEST_PREVIOUS_SEASON, previous=True)
        self.schedule = {day: [] for day in Weekday}
        self.user = User(
            daily_max_games=3,
            min_win_pct=0.4,
            win_pct_diff=0.2,
            min_watch_time=timedelta(hours=1),
            favorite_teams=["LAL", "DAL", "WAS", "PHI"],
            blocked_teams=["OKC"],
            schedule=self.schedule,
            simultaneous=False,
            win_pct_metric=bayesian_shrinkage
        )
        self.scheduler = Scheduler(self.user, self.test_games, get_standings_context(self.db))

    def tearDown(self):
        os.remove(self.db)


# redo these, think of TDD? external factors?
    # these deal with implementation, internals, and thus refactoring fails.
    def test_scheduler_adds_game_to_current_schedule(self):
        self.scheduler.add(0)
        self.assertEqual(self.scheduler._selected_games, [self.test_games[0]])

    def test_scheduler_adds_multiple_games_to_current_schedule(self):
        self.scheduler.add(0)
        self.scheduler.add(1)
        self.scheduler.add(7)
        self.assertEqual(self.scheduler._selected_games, [self.test_games[0], self.test_games[1], self.test_games[7]])

    def test_scheduler_removes_game_from_current_schedule(self):
        self.scheduler.add(1)
        self.scheduler.add(3)
        self.scheduler.remove(3)
        self.assertEqual(self.scheduler._selected_games, [self.test_games[1]])

    def test_scheduler_removes_multiple_games_from_current_schedule(self):
        self.scheduler.add(1)
        self.scheduler.add(3)
        self.scheduler.add(7)
        self.scheduler.remove(3)
        self.scheduler.remove(7)
        self.assertEqual(self.scheduler._selected_games, [self.test_games[1]])

    def test_scheduler_returns_empty_schedule(self):
        self.assertEqual(self.scheduler._selected_games, [])

    def test_scheduler_calculates_score_for_current_schedule(self):
        self.scheduler.add(1)
        expected_score = (50.0 + 15.0 + 12.465157 + 14.202962)
        self.assertAlmostEqual(self.scheduler.score, expected_score, places = 5)

    def test_scheduler_scores_zero_for_empty_schedule(self):
        self.assertEqual(self.scheduler.score, 0)

    def test_best_schedule_is_updated_as_current_schedule(self):
        self.scheduler.add(1)
        self.scheduler.add(3)
        self.scheduler.add(7)
        self.scheduler.update_best()
        self.assertEqual(self.scheduler._selected_games, self.scheduler._best_schedule)

    def test_scheduler_calculates_score_for_best_schedule(self):
        self.scheduler.add(7)
        self.scheduler.update_best()
        expected_score = (12.5 + 15.0 + 10.404891 + 11.452284)
        self.assertAlmostEqual(self.scheduler.best_score, expected_score, places = 5)

    def test_scheduler_scores_zero_without_best_schedule(self):
        self.assertEqual(self.scheduler.best_score, 0)

if __name__ == '__main__':
    unittest.main()
