from controllers.player import PlayerMenu
from controllers.tournament import TournamentMenu
from utils.tools import clear_console


class Home:
    def __init__(self, views):
        self.views = views
        self._player_menu = PlayerMenu(self.views)
        self._tournament_menu = TournamentMenu(self.views)

    @property
    def home_view(self):
        return self.views.home_view

    @property
    def title(self):
        return self.views.title_view

    def manager(self):
        clear_console()
        self.title.main_title()
        response = self.home_view.display_interface()
        if response == '0':
            self._player_menu.manager()
        if response == '1':
            self._tournament_menu.manager()
        if response == '9':
            exit()
