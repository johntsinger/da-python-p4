from models.storage import Storage
from models.player import PlayerInTournament
from models.exceptions import UserExitException
from controllers.create import NewTournament
from controllers.round import RoundController
from utils.tools import clear_console
from math import trunc


class TournamentMenu:
    def __init__(self, views, pretty_table):
        self.views = views
        self.pretty_table = pretty_table
        self.storage = Storage('tournaments')
        self.create_tournament = NewTournament(
            self.views, self.storage.all(), self.pretty_table)
        self.tournament_controller = TournamentController(
            self.views, self.pretty_table)

    @property
    def interface_view(self):
        return self.views.interface

    @property
    def create_view(self):
        return self.views.create

    @property
    def tournament_view(self):
        return self.views.tournament

    @property
    def title_view(self):
        return self.views.title

    def new_tournament(self):
        self.title_view.new_tournament()
        new_tournament = None
        # Exception raised if user type 'q' during creation
        try:
            new_tournament = self.create_tournament.create()
        except UserExitException:
            return None
        if new_tournament:
            if self.create_view.accept("tournament", new_tournament):
                new_tournament.uuid = self.storage.db.insert(
                    new_tournament.cleaned_data)
                self.storage.update(new_tournament)

    def select_tournament(self):
        tournaments = self.storage.all()
        if tournaments:
            self.pretty_table.display(tournaments)
            response = self.tournament_view.select('tournament')
            if response not in [str(tournament.uuid)
                                for tournament in tournaments]:
                return None
            if response:
                return self.storage.get_elt_by_id(int(response))
        return None

    def access_tournament(self):
        self.title_view.select_tournament()
        tournament = self.select_tournament()
        if tournament:
            self.tournament_controller.tournament = tournament
            self.tournament_controller.get_players_list()
            self.tournament_controller.manager()

    def delete_tournament(self):
        self.title_view.delete_tournament()
        tournament = self.select_tournament()
        if tournament:
            self.storage.remove(tournament)
            self.create_tournament.instances = self.storage.all()

    def manager(self):
        stay = True
        while stay:
            clear_console()
            self.title_view.tournament_menu()
            response = self.interface_view.display_interface('tournament')
            if response == '1':
                clear_console()
                self.new_tournament()
            elif response == '2':
                clear_console()
                self.access_tournament()
            elif response == '6':
                clear_console()
                self.delete_tournament()
            elif response == '9':
                stay = False


class TournamentController:
    def __init__(self, views, pretty_table):
        self.views = views
        self.pretty_table = pretty_table
        self.storage = Storage('tournaments')
        self._tournament = None
        self.round_controller = None
        self.players_list = None

    @property
    def interface_view(self):
        return self.views.interface

    @property
    def title_view(self):
        return self.views.title

    @property
    def tournament_view(self):
        return self.views.tournament

    @property
    def error_view(self):
        return self.views.error

    @property
    def tournament(self):
        return self._tournament

    @tournament.setter
    def tournament(self, value):
        self._tournament = value
        self.round_controller = RoundController(
            self.views, self._tournament, self.pretty_table)

    def start(self):
        if not self.tournament.rounds:
            self.adjust_number_of_round()
            self.round_controller.add_round()
        self.round_controller.manager()

    def max_round(self):
        """Find the maximun number of round a tournament can have.

        Divide the number of unique pairs by the number of matches per round
        """
        number_of_players = len(self.tournament.players)
        match_per_round = self.match_per_round(number_of_players)
        number_possible_matches = self.number_possible_matches(
            number_of_players)
        return trunc(number_possible_matches / match_per_round)

    @staticmethod
    def match_per_round(number_of_players):
        """Find the number of matches a round can have.

        If the number of players is odd, the single player is counted 
        as a match against 'EXEMPT', and 'EXEMPT' is counted as one player
        """
        if number_of_players % 2:
            number_of_matches = (number_of_players + 1) / 2
        else:
            number_of_matches = number_of_players / 2
        return number_of_matches

    @staticmethod
    def number_possible_matches(number_of_players):
        """Find the number of unique pairs in a set.

        formula : n!/k!(n-k)! where n is the number of items
        and k the number of elements in each set.
        Can be simplified to n(n-1)/2 if k=2
        """
        return (number_of_players * (number_of_players - 1)) / 2

    def adjust_number_of_round(self):
        max_round = self.max_round()
        if self.tournament.number_of_rounds > max_round:
            self.error_view.wrong_number_of_round(
                self.tournament.number_of_rounds,
                max_round
            )
            self.tournament.number_of_rounds = max_round
            self.views.wait.wait()

    def add_player(self):
        if not self.tournament.rounds:
            keep_selecting = True
            while self.players_list and keep_selecting:
                player = self.select_players()
                if player:
                    if player == 'q':
                        keep_selecting = False
                    else:
                        self.tournament.add_player(player)
                        self.storage.update(self.tournament)
            if not self.players_list:
                self.error_view.all_players_added()
                self.views.wait.wait()
        else:
            self.error_view.tournament_has_started()
            self.views.wait.wait()

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
        self.pretty_table.display(self.players_list)
        response = self.tournament_view.select('player')
        if response == 'q':
            return response
        if response not in [str(player.uuid)
                            for player in self.players_list]:
            self.error_view.player_not_exist(response)
            return None
        if response:
            for player in self.players_list:
                # not use players_list[int(response) - 1] because uuids may not 
                # follow each other if the object is deleted 
                # (i.e. : 1, 3 if 2 has been deleted)
                if player.uuid == int(response):
                    self.tournament_view.display_player(player)
                    self.players_list.remove(player)
                    return PlayerInTournament(player.last_name,
                                              player.first_name,
                                              player.date_of_birth,
                                              player.uuid)

    def display_players(self):
        self.title_view.players_list()
        players = self.tournament.players
        if players:
            players.sort(key=lambda obj: (obj.last_name, obj.first_name))
            self.pretty_table.display(players)
            self.views.wait.wait()

    def manager(self):
        stay = True
        while stay:
            clear_console()
            self.title_view.tournament_menu()
            self.pretty_table.display([self.tournament])
            response = self.interface_view.display_interface('tournament_menu')
            if response == '1':
                clear_console()
                self.add_player()
            elif response == '2':
                clear_console()
                self.start()
            elif response == '3':
                clear_console()
                self.display_players()
            elif response == '9':
                stay = False
