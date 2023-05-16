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

    @Validate._exists('tournament')
    def create(self):
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
        player = -1
        while player:
            player = self.select_players()
            if player:
                tournament.add_player(player)

    def get_players_list(self):
        storage = Storage('players').all()
        self.players_list = storage

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
