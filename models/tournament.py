from models.player import PlayerInTournament
from models.round import Round


class Tournament:
    """Model for a tournament"""
    def __init__(self, name, location, start_date, end_date,
                 description=None, number_of_rounds=4, rounds=None,
                 players=None, curent_round=0, uuid=None):

        self.uuid = uuid
        self.name = name
        self.location = location
        self._start_date = start_date
        self._end_date = end_date
        # avoid pitfall mutable defaut args
        self.players = players if players else []
        self.number_of_rounds = number_of_rounds
        self.rounds = rounds if rounds else []
        self.curent_round = curent_round
        self.description = description

    @property
    def start_date(self):
        return self._start_date.strftime('%d/%m/%Y %H:%M')

    @property
    def end_date(self):
        return self._start_date.strftime('%d/%m/%Y %H:%M')

    @property
    def cleaned_data(self):
        """Serialize object"""
        dictionary = {}
        for key, value in vars(self).items():
            key = key.lstrip('_')
            if isinstance(value, list):
                dictionary[key] = [elt.cleaned_data for elt in value]
            else:
                dictionary[key] = value
        return dictionary

    @classmethod
    def from_dict(cls, dictionary):
        """Deserialize object"""
        for key, value in dictionary.items():
            if key == "players":
                dictionary[key] = [
                    PlayerInTournament.from_dict(elt) for elt in value
                ]
            if key == "rounds":
                dictionary[key] = [
                    Round.from_dict(elt, dictionary['players'])
                    for elt in value
                ]
        return cls(**dictionary)

    def add_description(self, description):
        self.description = description

    def add_number_of_rounds(self, number_of_rounds):
        self.number_of_rounds = number_of_rounds

    def add_player(self, player):
        self.players.append(player)

    def add_round(self, round):
        self.rounds.append(round)

    def remove_player(self, player):
        self.players.remove(player)

    def __str__(self):
        string = ""
        for key, value in vars(self).items():
            if key.startswith("_"):
                key = key.lstrip("_")
                value = value.strftime('%d/%m/%Y %H:%M')
            if key == 'uuid':
                key = 'id'
            string += (f"{' '*8}{key.capitalize().replace('_', ' ')}"
                       f" : {value}\n")
        return string

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        """Compare another object to this tournament
        attributes compared :
            name, location and _start_date

        return :
            NotImplemented if wrong type or bool
        """
        if not isinstance(other, Tournament):
            return NotImplemented
        return all([self.name == other.name,
                    self.location == other.location,
                    self._start_date == other._start_date])
