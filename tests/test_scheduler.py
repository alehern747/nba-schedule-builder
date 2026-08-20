import unittest
import os
from schedule import Scheduler, Weekday
from test_data import TEST_GAMES, TEST_PREVIOUS_SEASON, TEST_TEAMS
from user import User
from standings import bayesian_shrinkage, get_standings_context
from datetime import timedelta
from database import create_database, save_standings
from scoring import calculate_score

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
            max_simultaneous_games=1,
            win_pct_metric=bayesian_shrinkage
        )
        self.scheduler = Scheduler(self.user, self.test_games, get_standings_context(self.db))

    def tearDown(self):
        os.remove(self.db)

    def test_scheduler_calculates_score_schedule(self):
        expected_score = (50.0 + 15.0 + 12.465157 + 14.202962)
        self.assertAlmostEqual(calculate_score(self.user, [self.test_games[1]], get_standings_context(self.db)), expected_score, places = 5)





if __name__ == '__main__':
    unittest.main()
