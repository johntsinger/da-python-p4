from views.error import ErrorView
from views.create import CreateView
from views.title import TitleView
from views.home import HomeView
from views.tournament import TournamentMenuView
from views.player import PlayerMenuView
from views.report import Report
from views.wait import WaitUserAction


class ViewsManager:
    def __init__(self):
        self.error_view = ErrorView()
        self.create_view = CreateView()
        self.title_view = TitleView()
        self.tournament_menu = TournamentMenuView()
        self.home_view = HomeView()
        self.player_menu = PlayerMenuView()
        self.report = Report()
        self.wait = WaitUserAction()
