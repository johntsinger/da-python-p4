from models.player import PlayerInTournament
from models.tournament import Tournament
from models.exceptions import UserExitException
from controllers.create.validate import Validate
from controllers.storage import Storage
from utils.tools import clear_console


class NewTournament(Validate):
    """Controller to create a new tournament"""
    def __init__(self, views, tournaments, pretty_table):
        super().__init__(views)
        self.pretty_table = pretty_table
        self.instances = tournaments
        self.players_list = None
        self.storage = Storage('temporary/tournament')
        self.storage.db.default_table_name = 'tournament'

    @property
    def tournament_view(self):
        return self.views.tournament

    @property
    def title_view(self):
        return self.views.title

    @Validate._exists('tournament')
    def base_data(self, data):
        """Get the data required to create a tournament"""
        try:
            data['name'] = self._input('str', 'Name') \
                if not data['name'] else data['name']
            data['location'] = self._input('str', 'Location') \
                if not data['location'] else data['location']
            data['start_date'] = self._input('date', 'Start date') \
                if not data['start_date'] else data['start_date']
            data['end_date'] = self._input('date', 'End date') \
                if not data['end_date'] else data['end_date']
        except UserExitException:
            if self.storage.db.all():
                self.storage.db.update(data)
            else:
                self.storage.db.insert(data)
            raise UserExitException
        else:
            return Tournament(**data)

    def get_additional_data(self, data):
        """Get additional data for the tournament"""
        try:
            if 'number_of_rounds' not in data:
                data['number_of_rounds'] = self._input(
                    'int',
                    'Number of rounds',
                    empty=True
                )
            data['description'] = self._input(
                'str',
                'Description of tournament',
                empty=True
            ) if 'description' not in data else data['description']
        except UserExitException:
            if 'number_of_rounds' in data and not data['number_of_rounds']:
                data['number_of_rounds'] = 4
            if self.storage.db.all():
                self.storage.db.update(data)
            else:
                self.storage.db.insert(data)
            raise UserExitException
        else:
            return data

    def create(self):
        """Create tournament object"""
        self.create_view.info('tournament')
        dictionary = {
            "name": None,
            "location": None,
            "start_date": None,
            "end_date": None
        }
        data = self.storage.db.all(
            )[0] if self.storage.db.all() else dictionary
        if data['name']:
            response = self.create_view.load_data('tournament', data)
            if not response:
                data = dictionary
                self.storage.db.truncate()
        tournament = self.base_data(data)

        if tournament:
            additional_data = self.get_additional_data(data)
            if additional_data['number_of_rounds']:
                tournament.add_number_of_rounds(
                    additional_data['number_of_rounds'])
            if additional_data['description']:
                tournament.add_description(additional_data['description'])
            self.add_player(tournament)
        else:
            self.views.wait.wait()
        self.storage.db.truncate()
        return tournament

    def add_player(self, tournament):
        """Add player in this tournament"""
        self.get_players_list()
        keep_selecting = True
        while self.players_list and keep_selecting:
            self.create_view.add_player()
            player = self.select_player()
            if player:
                if player == 'q':
                    keep_selecting = False
                else:
                    tournament.add_player(player)
        if not self.players_list:
            self.error_view.all_players_added()
            self.views.wait.wait()

    def get_players_list(self):
        """Get all player registered in the system"""
        storage = Storage('players').all()
        self.players_list = storage

    def select_player(self):
        self.pretty_table.display(self.players_list)
        response = self.tournament_view.select('player')
        clear_console()
        self.title_view.new_tournament()
        if response == 'q':
            return response
        if response in [str(player.uuid)
                        for player in self.players_list]:
            for player in self.players_list:
                if player.uuid == int(response):
                    self.tournament_view.display_player(player)
                    self.players_list.remove(player)
                    return PlayerInTournament(player.last_name,
                                              player.first_name,
                                              player.date_of_birth,
                                              player.uuid)
        self.error_view.player_not_exist(response)
        return None
