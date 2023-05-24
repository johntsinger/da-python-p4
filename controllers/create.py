from models.player import Player, PlayerInTournament
from models.tournament import Tournament
from controllers.validate import Validate
from models.storage import Storage


class NewPlayer(Validate):
    def __init__(self, views, players):
        super().__init__(views)
        self.instances = players

    @Validate._exists('player')
    def create(self):
        self.views.create_view.title('player')
        last_name = self._input('str', 'Last name')
        first_name = self._input('str', 'First name')
        date_of_birth = self._input('date', 'Date of birth')
        player = Player(last_name, first_name, 
                        date_of_birth)
        return player


class NewTournament(Validate):
    def __init__(self, views, tournaments):
        super().__init__(views)
        self.instances = tournaments
        self.players_list = None

    @property
    def report(self):
        return self.views.report

    @property
    def tournament_menu(self):
        return self.views.tournament_menu

    @property
    def error_view(self):
        return self.views.error_view

    @Validate._exists('tournament')
    def create(self):
        self.views.create_view.title('tournament')
        name = self._input('str', 'Name')
        location = self._input('str', 'Location')
        start_date = self._input('date', 'Start date')
        end_date = self._input('date', 'End date')
        number_of_rounds = self._input(
            'int',
            'Number of rounds (can be left empty (default 4 rounds)',
            empty=True
        )
        description = self._input(
            'str',
            "Description of tournament",
            empty=True)
        tournament = Tournament(name, location, start_date,
                                end_date)
        # set args that have a default value
        if number_of_rounds:
            tournament.set_number_of_rounds(number_of_rounds)
        if description:
            tournament.set_description(description)
        self.add_player(tournament)
        return tournament

    def add_player(self, tournament):
        self.get_players_list()
        keep_selecting = True
        while self.players_list and keep_selecting:
            player = self.select_players()
            if player:
                if player == 'q':
                    keep_selecting = False
                else:
                    tournament.add_player(player)
        if not self.players_list:
            self.error_view.all_players_added()
            self.views.wait.wait()

    def get_players_list(self):
        storage = Storage('players').all()
        self.players_list = storage

    def select_players(self):
        if self.players_list:
            self.report.display_all(self.players_list)
            response = self.tournament_menu.select('player')
            if response == 'q':
                return response
            if response not in [str(player.uuid) 
                                for player in self.players_list]:
                self.error_view.player_not_exist(response)
                return None
            if response:
                for player in self.players_list:
                    if player.uuid == int(response):
                        self.tournament_menu.display_player(player)
                        self.views.wait.wait()
                        self.players_list.remove(player)
                        return PlayerInTournament(player.last_name,
                                                  player.first_name,
                                                  player.date_of_birth,
                                                  player.uuid)
        self.error_view.all_players_added()
        self.views.wait.wait()
