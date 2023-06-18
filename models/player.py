import dateutil.parser


class Player:
    """Model for a player"""
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
        """Serialize object"""
        return {
            key.lstrip("_"): value for key, value in vars(self).items()
        }

    @classmethod
    def from_dict(cls, dictionary):
        """Deserialize object"""
        return cls(**dictionary)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.date_of_birth}"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        """Compare another object to this player
        attributes compared :
            last_name, first_name and _date_of_birth

        return :
            NotImplemented if wrong type or bool
        """
        if not isinstance(other, (Player, PlayerInTournament)):
            return NotImplemented
        return all([self.last_name == other.last_name,
                    self.first_name == other.first_name,
                    self._date_of_birth == other._date_of_birth])


class PlayerInTournament(Player):
    """Model for player in tournament"""
    def __init__(self, last_name, first_name, date_of_birth, uuid,
                 score=0, cumulative_list=None, cumulative_score=0,
                 buchholz_score=0, withdrawal=False):
        super().__init__(last_name, first_name, date_of_birth, uuid)
        self.score = score
        self.cumulative_list = cumulative_list if cumulative_list else []
        self.cumulative_score = cumulative_score
        self.buchholz_score = buchholz_score
        self.withdrawal = withdrawal  # if player leaves the tournament
        if isinstance(self._date_of_birth, str):
            self._date_of_birth = dateutil.parser.parse(self._date_of_birth)

    def display_without_score(self):
        return f"{self.last_name} {self.first_name}"

    def __repr__(self):
        return str(self)

    def __str__(self):
        tie_breaking_display = (f" (Bu. {self.buchholz_score}"
                                f" Cu. {self.cumulative_score})")
        return (f"{self.first_name} {self.last_name}"
                f" {self.score if not self.withdrawal else '(withdrawal)'}"
                f"{tie_breaking_display if not self.withdrawal else ''}")
