class Player:

    def __init__(self, last_name, first_name, date_of_birth, uuid=None):
        self.uuid = uuid
        self.last_name = last_name
        self.first_name = first_name
        self._date_of_birth = date_of_birth

    @property
    def date_of_birth(self):
        return self._date_of_birth.strftime('%d/%m/%Y')

    @property
    def cleaned_data(self):
        return {
            key.lstrip("_"): value for key, value in vars(self).items()
        }

    @classmethod
    def from_dict(cls, dictionary):
        return Player(**dictionary)
    
    def __str__(self):
        string = ""
        for key, value in vars(self).items():
            if key.startswith("_"):
                key = key.lstrip("_")
                if not isinstance(value, str):
                    value = value.strftime('%d/%m/%Y')
            if key == 'uuid':
                key = 'Id'
            string += f"{key.capitalize().replace('_', ' ')} : {value}\n"
        return string

    def __repr__(self):
        return (f"Player(last_name={self.last_name}, "
                f"first_name={self.first_name}, "
                f"date_of_birth={self.date_of_birth})")

    def __eq__(self, other):
        if not isinstance(other, Player):
            return NotImplemented
        return all([self.last_name == other.last_name,
                    self.first_name == other.first_name,
                    self._date_of_birth == other._date_of_birth])


class PlayerInTournament(Player):
    def __init__(self, last_name, first_name, date_of_birth, uuid, score=0,
                 opponents=None):
        super().__init__(last_name, first_name, date_of_birth, uuid)
        self.score = score
        self.opponents = opponents if opponents else []

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
            if key == "opponents":
                dictionary[key] = [
                    PlayerInTournament.from_dict(elt) for elt in value
                ]
        return PlayerInTournament(**dictionary)

    def __repr__(self):
        return f"{self.last_name} {self.first_name}"
