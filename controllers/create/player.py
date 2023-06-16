from models.player import Player
from controllers.create.validate import Validate
from controllers.storage import Storage
from models.exceptions import UserExitException


class NewPlayer(Validate):
    """Controller to create a new player"""
    def __init__(self, views, players):
        super().__init__(views)
        self.instances = players
        self.storage = Storage('temporary/player')
        self.storage.db.default_table_name = 'player'

    @Validate._exists('player')
    def base_data(self, data):
        """Get the data required to create a player.
        Save the data in temporary file if user exit the creation

        params:
            - data (dict) : a dictionary with temporary data to continue
                            an older creation if one exists
        """
        try:
            data['last_name'] = self._input('str', 'Last name') \
                if not data['last_name'] else data['last_name']
            data['first_name'] = self._input('str', 'First name') \
                if not data['first_name'] else data['first_name']
            data['date_of_birth'] = self._input('date', 'Date of birth') \
                if not data['date_of_birth'] else data['date_of_birth']
        except UserExitException:
            if self.storage.db.all():
                self.storage.db.update(data)
            else:
                self.storage.db.insert(data)
            raise UserExitException
        else:
            player = Player(**data)
            return player

    def create(self):
        """Create player object"""
        self.create_view.info('player')
        dictionary = {
            "last_name": None,
            "first_name": None,
            "date_of_birth": None
        }
        data = self.storage.db.all(
            )[0] if self.storage.db.all() else dictionary
        if data['last_name']:
            response = self.create_view.load_data('player', data)
            if not response:
                data = dictionary
                self.storage.db.truncate()
        player = self.base_data(data)
        if not player:
            self.views.wait.wait()
        self.storage.db.truncate()
        return player
