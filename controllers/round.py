from random import shuffle
from models.round import Round
from models.match import Match


class RoundController:
    def __init__(self, views, tournament):
        self.views = views
        self.tournament = tournament
        self.round = None

    @property
    def round_view(self):
        return self.views.round_view

    @property
    def report(self):
        return self.views.report

    def generate(self):
        players_list = self.tournament.players
        round_name = f'Round {self.tournament.curent_round}'
        self.round = Round(round_name)
        if self.tournament.curent_round == 1:
            shuffle(players_list)
            for pair in self.get_pair(players_list):
                match = Match(*pair)
                self.round.matches.append(match)
        else:
            players_list.sort(key=lambda obj: obj.score, reverse=True)
            for pair in self.get_pair(players_list):
                match = Match(*pair)
                self.round.matches.append(match)
        self.tournament.rounds.append(self.round)

    def get_pair(self, players_list):
        iterator = iter(players_list)
        for player in iterator:
            try:
                yield (player, next(iterator))
            except StopIteration:
                yield (player, 'EXEMPT')

    def select_winner(self):
        for match in self.round.matches:
            players = [match.player_1, match.player_2]
            self.round_view.prompt_for_winner(match)
            self.report.display_all([match])
            if isinstance(match.player_2, str):
                match.winner = match.player_1
            else:
                response = self.round_view.select('winner')
                if response in ["1", "2", "3"]:
                    if response == '3':
                        match.winner = [match.player_1, match.player_2]
                    else:
                        match.winner = players[int(response) - 1]
