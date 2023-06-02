from controllers.player import PlayerMenu
from controllers.tournament import TournamentMenu
from controllers.prettytable import MyPrettyTable
from utils.tools import clear_console


class Home:
    def __init__(self, views):
        self.views = views
        self.pretty_table = MyPrettyTable(self.views)
        self._player_menu = PlayerMenu(self.views, self.pretty_table)
        self._tournament_menu = TournamentMenu(self.views, self.pretty_table)

    @property
    def interface(self):
        return self.views.interface

    @property
    def title(self):
        return self.views.title_view

    def manager(self):
        clear_console()
        self.title.main_title()
        response = self.interface.display_interface('home')
        if response == "1":
            self._player_menu.manager()
        elif response == "2":
            self._tournament_menu.manager()
        elif response == "9":
            exit()
