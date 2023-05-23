from models.player import PlayerInTournament
from models.round import Round


class Tournament:
    def __init__(self, name, location, start_date, end_date,
                 description=None, number_of_rounds=4, rounds=None,
                 players=None, curent_round=0, uuid=None):

        self.uuid = uuid
        self.name = name
        self.location = location
        self._start_date = start_date
        self._end_date = end_date
        self.number_of_rounds = number_of_rounds
        self.rounds = rounds if rounds else []  # avoid pifall mutable defaut args
        self.players = players if players else []
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
        for key, value in dictionary.items():
            if key == "rounds":
                dictionary[key] = [Round.from_dict(elt) for elt in value]
            if key == "players":
                dictionary[key] = [PlayerInTournament.from_dict(elt) for elt in value]
        return Tournament(**dictionary)

    def set_description(self, description):
        self.description = description

    def set_number_of_rounds(self, number_of_rounds):
        self.number_of_rounds = number_of_rounds

    def add_player(self, player):
        self.players.append(player)

    def add_round(self, round):
        self.rounds.append(round)

    def __str__(self):
        string = ""
        for key, value in vars(self).items():
            if key.startswith("_"):
                key = key.lstrip("_")
                value = value.strftime('%d/%m/%Y %H:%M')
            if key == 'uuid':
                key = 'id'
            string += f"{' '*8}{key.capitalize().replace('_', ' ')} : {value}\n"
        return string

    def __repr__(self):
        return (f"Tournament(id={self.uuid}, "
                f"name={self.name}, "
                f"location={self.location}, "
                f"start_date={self.start_date}, "
                f"end_date={self.end_date}, "
                f"number_of_rounds={self.number_of_rounds}, "
                f"rounds={self.rounds}, "
                f"players={self.players}, "
                f"curent_round={self.curent_round}, "
                f"description={self.description}")

    def __eq__(self, other):
        if not isinstance(other, Tournament):
            return NotImplemented
        return all([self.name == other.name,
                    self.location == other.location,
                    self._start_date == other._start_date])
