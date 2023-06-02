from views.error import ErrorView
from views.create import CreateView
from views.title import TitleView
from views.interface import InterfaceView
from views.tournament import TournamentMenuView
from views.player import PlayerMenuView
from views.prettytable import TableView
from views.wait import WaitUserAction
from views.round import RoundView


class ViewsManager:
    def __init__(self):
        self.error_view = ErrorView()
        self.create_view = CreateView()
        self.title_view = TitleView()
        self.tournament_menu = TournamentMenuView()
        self.player_menu = PlayerMenuView()
        self.table_view = TableView()
        self.wait = WaitUserAction()
        self.round_view = RoundView()
        self.interface = InterfaceView()
