from models.storage import Storage
from models.player import PlayerInTournament
from controllers.create import NewTournament
from controllers.round import RoundController
from utils.tools import clear_console


class TournamentMenu:
    def __init__(self, views):
        self.views = views
        self.storage = Storage('tournaments')
        self.create_tournament = NewTournament(self.views, self.storage.all())
        self.tournament_controller = TournamentController(self.views)

    @property
    def create_view(self):
        return self.views.create_view

    @property
    def tournament_menu(self):
        return self.views.tournament_menu

    @property
    def title(self):
        return self.views.title_view

    @property
    def report(self):
        return self.views.report

    def new_tournament(self):
        self.title.new_tournament_title()
        new_tournament = self.create_tournament.create()
        if new_tournament:
            if self.create_view.accept("tournament", new_tournament):
                new_tournament.uuid = self.storage.db.insert(
                    new_tournament.cleaned_data)
                self.storage.update(new_tournament)
                return new_tournament

    def select_tournament(self):
        tournaments = self.storage.all()
        if tournaments:
            self.report.display_all(tournaments)
            response = self.tournament_menu.select('tournament')
            if response not in [str(tournament.uuid)
                                for tournament in tournaments]:
                return None
            if response:
                self.views.wait.wait()
                return self.storage.all()[int(response) - 1]
        return None

    def manager(self):
        stay = True
        while stay:
            clear_console()
            self.title.tournament_menu()
            response = self.tournament_menu.display_menu_interface()
            if response == '0':
                clear_console()
                self.new_tournament()
            if response == '1':
                clear_console()
                tournament = self.select_tournament()
                if tournament:
                    self.tournament_controller.tournament = tournament
                    self.tournament_controller.get_players_list()
                    self.tournament_controller.manager()
            if response == '6':
                tournament = self.select_tournament()
                if tournament:
                    self.storage.remove(tournament)
            if response == '9':
                stay = False


class TournamentController:
    def __init__(self, views):
        self.views = views
        self.storage = Storage('tournaments')
        self._tournament = None
        self.round = None
        self.players_list = None

    @property
    def report(self):
        return self.views.report

    @property
    def title(self):
        return self.views.title_view

    @property
    def tournament_menu(self):
        return self.views.tournament_menu

    @property
    def error_view(self):
        return self.views.error_view

    @property
    def tournament(self):
        return self._tournament

    @tournament.setter
    def tournament(self, value):
        self._tournament = value
        self.round = RoundController(self.views, self._tournament)

    def start(self):
        pass

    def add_player(self, player):
        self.tournament.add_player(player)
        self.storage.update(self.tournament)

    def get_rounds(self):
        self.round.generate()
        self.storage.update(self.tournament)

    def get_players_list(self):
        storage = Storage('players').all()
        set1 = set(player_in_tournament.uuid for player_in_tournament 
                   in self.tournament.players)
        self.players_list = [
            player for player 
            in storage 
            if player.uuid not in set1
        ]

    def select_players(self):
        if self.players_list:
            self.report.display_all(self.players_list)
            response = self.tournament_menu.select('player')
            if response not in [str(player.uuid)
                                for player in self.players_list]:
                return None
            if response:
                for player in self.players_list:
                    if player.uuid == int(response):
                        print(player)
                        self.views.wait.wait()
                        self.players_list.remove(player)
                        return PlayerInTournament(player.last_name,
                                                  player.first_name,
                                                  player.date_of_birth,
                                                  player.uuid)
        self.error_view.all_players_added()
        self.views.wait.wait()

    def display(self, obj):
        for key, value in vars(obj).items():
            print(key, value, type(value))
            if isinstance(value, list):
                for elt in value:
                    self.display(elt)

    def manager(self):
        stay = True
        while stay:
            clear_console()
            self.title.tournament_menu()
            self.report.display_all([self.tournament])
            response = self.tournament_menu.display_interface()
            if response == '0':
                clear_console()
                player = self.select_players()
                if player:
                    self.add_player(player)
            if response == '1':
                clear_console()
                self.get_rounds()
                self.views.wait.wait()
            if response == '9':
                stay = False
