from models.player import PlayerInTournament


class Match:
    G = "\033[0;32;40m"  # GREEN
    N = "\033[0m"  # Reset

    def __init__(self, uuid, player_1, player_2,
                 score_player_1=0, score_player_2=0, winner=None):
        self.uuid = uuid
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
            for player in value:
                player.score += 0.5
            self.score_player_1 = 0.5
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
    def from_dict(cls, dictionary, players):
        for key, value in dictionary.items():
            if key == 'winner':
                players_to_add = []
                if isinstance(value, list):
                    for elt in value:
                        player_from_dict = PlayerInTournament.from_dict(elt)
                        for player in players:
                            if player_from_dict == player:
                                players_to_add.append(player)
                                break
                    dictionary[key] = players_to_add
                elif value:
                    player_from_dict = PlayerInTournament.from_dict(value)
                    for player in players:
                        if player == player_from_dict:
                            dictionary[key] = player
                            break
            else:
                if not isinstance(value, (str, int, float)):
                    player_from_dict = PlayerInTournament.from_dict(value)
                    for player in players:
                        if player_from_dict == player:
                            dictionary[key] = player
                            break
        return cls(**dictionary)

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
            player_2_str = (f"{self.score_player_2} "
                            f"{self.player_2.last_name} "
                            f"{self.player_2.first_name}")
        if self.player_1 == self.winner:
            player_1_str = self.G+player_1_str+self.N
        elif isinstance(self.winner, list):
            player_1_str = self.G+player_1_str+self.N
            player_2_str = self.G+player_2_str+self.N
        elif self.player_2 == self.winner:
            player_2_str = self.G+player_2_str+self.N

        return f"{player_1_str} - {player_2_str}"

    def __eq__(self, other):
        if not isinstance(other, Match):
            return NotImplemented
        return (
            self.player_1 == other.player_1 or self.player_1 == other.player_2
        ) and (
            self.player_2 == other.player_1 or self.player_2 == other.player_2
        )
