from random import shuffle
from models.round import Round
from models.match import Match


class RoundController:
    def __init__(self, views, tournament):
        self.views = views
        self.tournament = tournament

    def generate(self):
        players_list = self.tournament.players
        _round = Round('Round 1')
        if self.tournament.curent_round == 1:
            shuffle(players_list)
            for pair in self.get_pair(players_list):
                match = Match(*pair)
                _round.matches.append(match)
        else:
            players_list = self.sort_players(players_list)
            for pair in self.get_pair(players_list):
                match = Match(*pair)
                _round.matches.append(match)
        self.tournament.rounds.append(_round)

    def sort_players(self, players_list):
        return players_list.sort(key=lambda obj: obj.score)

    def get_pair(self, players_list):
        iterator = iter(players_list)
        for player in iterator:
            try:
                yield (player, next(iterator))
            except StopIteration:
                yield (player, 'EXEMPT')
