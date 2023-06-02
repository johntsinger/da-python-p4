from views.error import ErrorView
from views.create import CreateView
from views.title import TitleView
from views.interface import InterfaceView
from views.tournament import TournamentMenuView
from views.player import PlayerMenuView
from views.prettytable import PrettyTableView
from views.wait import WaitUserAction
from views.round import RoundView


class ViewsManager:
    def __init__(self):
        self.error = ErrorView()
        self.create = CreateView()
        self.title = TitleView()
        self.tournament = TournamentMenuView()
        self.player = PlayerMenuView()
        self.pretty_table = PrettyTableView()
        self.wait = WaitUserAction()
        self.round = RoundView()
        self.interface = InterfaceView()
