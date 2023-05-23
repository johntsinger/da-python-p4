from models.player import PlayerInTournament


class Match:
    def __init__(self, player_1, player_2, score_player_1=0, score_player_2=0, winner=None):
        self.player_1 = player_1
        self.player_2 = player_2
        self.score_player_1 = score_player_1
        self.score_player_2 = score_player_2
        self._winner = winner

    @property
    def winner(self):
        return self._winner

    @winner.setter
    def winner(self, value):
        if isinstance(value, list):
            self.player_1.score += 0.5
            self.score_player_1 = 0.5
            self.player_2.score += 0.5
            self.score_player_2 = 0.5
            self._winner = value
        else:
            value.score += 1
            if value == self.player_1:
                self.score_player_1 = 1
            if value == self.player_2:
                self.score_player_2 = 1
            self._winner = value

    @property
    def cleaned_data(self):
        dictionary = {}
        for key, value in vars(self).items():
            key = key.lstrip('_')
            if isinstance(value, PlayerInTournament):
                dictionary[key] = value.cleaned_data
            elif isinstance(value, list):
                dictionary[key] = [elt.cleaned_data for elt in value]
            else:
                dictionary[key] = value
        return dictionary

    @classmethod
    def from_dict(cls, dictionary):
        for key, value in dictionary.items():
            if key == 'winner':
                if isinstance(value, list):
                    dictionary[key] = [PlayerInTournament.from_dict(elt) for elt in value]
            else:
                if not isinstance(value, (str, int, float)):
                    dictionary[key] = PlayerInTournament.from_dict(value)
        return Match(**dictionary)

    @property
    def as_tuple(self):
        return ([self.player_1, self.player_1.score],
                [self.player_2, self.player_2.score] 
                if not isinstance(self.player_2, str) else [self.player_2])

    def __repr__(self):
        player_1_str = (f"{self.player_1.last_name} " 
                        f"{self.player_1.first_name} " 
                        f"{self.score_player_1}")
        player_2_str = self.player_2
        if not isinstance(self.player_2, str):
            player_2_str = (f"{self.player_2.last_name} "
                            f"{self.player_2.first_name} "
                            f"{self.score_player_2}")

        return f"([{player_1_str}][{player_2_str}])"

    def __eq__(self, other):
        if not isinstance(other, Match):
            return NotImplemented
        return (
            self.player_1 == other.player_1 or self.player_1 == other.player_2
        ) and (
            self.player_2 == other.player_1 or self.player_2 == other.player_2
        )
