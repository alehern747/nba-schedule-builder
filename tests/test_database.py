import unittest
import os
from teams import Team
from datetime import datetime
from src.database import (create_database, save_standings, save_games, update_last_refresh,
                          retrieve_last_refresh, retrieve_standings, retrieve_processed_games, delete_season)


class DatabaseTest(unittest.TestCase):
    def setUp(self):
        self.db = "test.db"
        create_database(self.db)

    def tearDown(self):
        os.remove(self.db)

    def test_save_games(self):
        save_games(self.db, [18446917, 18446918, 18446919])
        processed = retrieve_processed_games(self.db)
        self.assertEqual(processed, {18446917, 18446918, 18446919})

    def test_save_standings(self):
        test_standings = [Team("ATL", "East", 3, 3, 0.0), Team("LAL", "West", 6, 0, 0.0),
                                 Team("GSW", "West", 0, 6, 0.0)]
        save_standings(self.db, test_standings)
        standings = retrieve_standings(self.db)
        self.assertEqual(standings, {"ATL": test_standings[0], "LAL": test_standings[1], "GSW": test_standings[2]})

    def test_save_last_refresh(self):
        update_last_refresh(self.db)
        self.assertEqual(retrieve_last_refresh(self.db), datetime.now().isoformat(timespec = 'minutes'))

if __name__ == '__main__':
    unittest.main()
