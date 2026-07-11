import datetime
from games import Game

TEST_GAMES = [
    Game(id=18446819, datetime=datetime.datetime(2025, 10, 21, 16, 30, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=61200), 'PDT')), home_team='OKC', away_team='HOU', postseason=False),
    Game(id=18446820, datetime=datetime.datetime(2025, 10, 21, 19, 0, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=61200), 'PDT')), home_team='LAL', away_team='GSW', postseason=False),
    Game(id=18446821, datetime=datetime.datetime(2025, 10, 22, 16, 0, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=61200), 'PDT')), home_team='NYK', away_team='CLE', postseason=False),
    Game(id=18446822, datetime=datetime.datetime(2025, 10, 22, 18, 30, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=61200), 'PDT')), home_team='DAL', away_team='SAS', postseason=False),
    Game(id=18446823, datetime=datetime.datetime(2025, 10, 22, 16, 0, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=61200), 'PDT')), home_team='CHA', away_team='BKN', postseason=False),
    Game(id=18446824, datetime=datetime.datetime(2025, 10, 22, 16, 0, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=61200), 'PDT')), home_team='ORL', away_team='MIA', postseason=False),
    Game(id=18446825, datetime=datetime.datetime(2025, 10, 22, 16, 30, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=61200), 'PDT')), home_team='ATL', away_team='TOR', postseason=False),
    Game(id=18446826, datetime=datetime.datetime(2025, 10, 22, 16, 30, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=61200), 'PDT')), home_team='BOS', away_team='PHI', postseason=False),
    Game(id=18446827, datetime=datetime.datetime(2025, 10, 22, 17, 0, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=61200), 'PDT')), home_team='CHI', away_team='DET', postseason=False),
    Game(id=18446828, datetime=datetime.datetime(2025, 10, 22, 17, 0, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=61200), 'PDT')), home_team='MEM', away_team='NOP', postseason=False),
    Game(id=18446829, datetime=datetime.datetime(2025, 10, 22, 17, 0, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=61200), 'PDT')), home_team='MIL', away_team='WAS', postseason=False),
    Game(id=18446830, datetime=datetime.datetime(2025, 10, 22, 18, 0, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=61200), 'PDT')), home_team='UTA', away_team='LAC', postseason=False),
    Game(id=18446831, datetime=datetime.datetime(2025, 10, 22, 19, 0, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=61200), 'PDT')), home_team='PHX', away_team='SAC', postseason=False),
    Game(id=18446832, datetime=datetime.datetime(2025, 10, 22, 19, 0, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=61200), 'PDT')), home_team='POR', away_team='MIN', postseason=False)
]