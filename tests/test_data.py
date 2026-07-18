import datetime
from games import Game
from teams import Team

TEST_GAMES = [
    Game(id=18446819, datetime=datetime.datetime(2025, 10, 21, 16, 30, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=61200), 'PDT')), home_team='OKC', away_team='HOU', home_score=125, away_score=124, status='Final', postseason=False),
    Game(id=18446820, datetime=datetime.datetime(2025, 10, 21, 19, 0, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=61200), 'PDT')), home_team='LAL', away_team='GSW', home_score=109, away_score=119, status='Final', postseason=False),
    Game(id=18446821, datetime=datetime.datetime(2025, 10, 22, 16, 0, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=61200), 'PDT')), home_team='NYK', away_team='CLE', home_score=119, away_score=111, status='Final', postseason=False),
    Game(id=18446822, datetime=datetime.datetime(2025, 10, 22, 18, 30, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=61200), 'PDT')), home_team='DAL', away_team='SAS', home_score=92, away_score=125, status='Final', postseason=False),
    Game(id=18446823, datetime=datetime.datetime(2025, 10, 22, 16, 0, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=61200), 'PDT')), home_team='CHA', away_team='BKN', home_score=136, away_score=117, status='Final', postseason=False),
    Game(id=18446824, datetime=datetime.datetime(2025, 10, 22, 16, 0, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=61200), 'PDT')), home_team='ORL', away_team='MIA', home_score=125, away_score=121, status='Final', postseason=False),
    Game(id=18446825, datetime=datetime.datetime(2025, 10, 22, 16, 30, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=61200), 'PDT')), home_team='ATL', away_team='TOR', home_score=118, away_score=138, status='Final', postseason=False),
    Game(id=18446826, datetime=datetime.datetime(2025, 10, 22, 16, 30, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=61200), 'PDT')), home_team='BOS', away_team='PHI', home_score=116, away_score=117, status='Final', postseason=False),
    Game(id=18446827, datetime=datetime.datetime(2025, 10, 22, 17, 0, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=61200), 'PDT')), home_team='CHI', away_team='DET', home_score=115, away_score=111, status='Final', postseason=False),
    Game(id=18446828, datetime=datetime.datetime(2025, 10, 22, 17, 0, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=61200), 'PDT')), home_team='MEM', away_team='NOP', home_score=128, away_score=122, status='Final', postseason=False),
    Game(id=18446829, datetime=datetime.datetime(2025, 10, 22, 17, 0, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=61200), 'PDT')), home_team='MIL', away_team='WAS', home_score=133, away_score=120, status='Final', postseason=False),
    Game(id=18446830, datetime=datetime.datetime(2025, 10, 22, 18, 0, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=61200), 'PDT')), home_team='UTA', away_team='LAC', home_score=129, away_score=108, status='Final', postseason=False),
    Game(id=18446831, datetime=datetime.datetime(2025, 10, 22, 19, 0, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=61200), 'PDT')), home_team='PHX', away_team='SAC', home_score=120, away_score=116, status='Final', postseason=False),
    Game(id=18446832, datetime=datetime.datetime(2025, 10, 22, 19, 0, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=61200), 'PDT')), home_team='POR', away_team='MIN', home_score=114, away_score=118, status='Final', postseason=False)
]

TEST_TEAMS = [
    Team(name = "ATL", conference = "East", wins = 4, losses = 4, win_pct = 0.5),
    Team(name = "BOS", conference = "East", wins = 3, losses = 5, win_pct = 0.375),
    Team(name = "BKN", conference = "East", wins = 0, losses = 7, win_pct = 0),
    Team(name = "CHA", conference = "East", wins = 3, losses = 5, win_pct = 0.375),
    Team(name = "CHI", conference = "East", wins = 6, losses = 1, win_pct = 0.857),
    Team(name = "CLE", conference = "East", wins = 4, losses = 3, win_pct = 0.571),
    Team(name = "DAL", conference = "West", wins = 2, losses = 5, win_pct = 0.286),
    Team(name = "DEN", conference = "West", wins = 4, losses = 2, win_pct = 0.667),
    Team(name = "DET", conference = "East", wins = 5, losses = 2, win_pct = 0.714),
    Team(name = "GSW", conference = "West", wins = 5, losses = 3, win_pct = 0.625),
    Team(name = "HOU", conference = "West", wins = 4, losses = 2, win_pct = 0.667),
    Team(name = "IND", conference = "East", wins = 1, losses = 6, win_pct = 0.143),
    Team(name = "LAC", conference = "West", wins = 3, losses = 4, win_pct = 0.429),
    Team(name = "LAL", conference = "West", wins = 6, losses = 2, win_pct = 0.75),
    Team(name = "MEM", conference = "West", wins = 3, losses = 5, win_pct = 0.375),
    Team(name = "MIA", conference = "East", wins = 4, losses = 3, win_pct = 0.571),
    Team(name = "MIL", conference = "East", wins = 5, losses = 3, win_pct = 0.625),
    Team(name = "MIN", conference = "West", wins = 4, losses = 3, win_pct = 0.571),
    Team(name = "NOP", conference = "West", wins = 1, losses = 6, win_pct = 0.143),
    Team(name = "NYK", conference = "East", wins = 4, losses = 3, win_pct = 0.571),
    Team(name = "OKC", conference = "West", wins = 8, losses = 0, win_pct = 1),
    Team(name = "ORL", conference = "East", wins = 3, losses = 5, win_pct = 0.375),
    Team(name = "PHI", conference = "East", wins = 5, losses = 2, win_pct = 0.714),
    Team(name = "PHX", conference = "West", wins = 3, losses = 5, win_pct = 0.375),
    Team(name = "POR", conference = "West", wins = 4, losses = 3, win_pct = 0.571),
    Team(name = "SAC", conference = "West", wins = 2, losses = 5, win_pct = 0.286),
    Team(name = "SAS", conference = "West", wins = 5, losses = 1, win_pct = 0.833),
    Team(name = "TOR", conference = "East", wins = 4, losses = 4, win_pct = 0.5),
    Team(name = "UTA", conference = "West", wins = 3, losses = 4, win_pct = 0.429),
    Team(name = "WAS", conference = "East", wins = 1, losses = 6, win_pct = 0.143)
]