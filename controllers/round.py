from random import shuffle
from models.round import Round
from models.match import Match
from models.storage import Storage


class NewRound:
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
        players_list = list(self.tournament.players)
        self.tournament.curent_round += 1
        round_name = f'Round {self.tournament.curent_round}'
        self.round = Round(round_name)
        if self.tournament.curent_round == 1:
            shuffle(players_list)
            for match in self.get_pair(players_list):
                #match = Match(*pair)
                self.round.matches.append(match)
        else:
            players_list.sort(key=lambda obj: obj.score, reverse=True)
            if len(players_list) % 2:
                number_of_matches = len(players_list + 1) / 2
            else:
                number_of_matches = len(players_list) / 2
            matches = self.get_pair(players_list)
            print('first pair matches : ', matches)
            if len(matches) < number_of_matches:
                players_list = list(self.tournament.players)
                print("NUMBER OF MATCH MISS")
                players_list.sort(key=lambda obj: obj.score)
                matches = self.get_pair(players_list)
                print('Second pair matches', matches)
                self.views.wait.wait()
            for match in matches:
                #match = Match(*pair)
                self.round.matches.append(match)
        self.tournament.rounds.append(self.round)
        return self.round

    def get_pair(self, players_list):
        pair = []
        while players_list:
            player_1 = players_list.pop(0)
            if players_list:
                for player_2 in players_list:
                    match = Match(*(player_1, player_2))
                    if self.match_exists(match):
                        continue
                    pair.append(match)
                    break
                players_list.remove(player_2)
            else:
                player_2 = "EXEMPT"
                match = Match(*(player_1, player_2))
                pair.append(match)
        return pair

    def match_exists(self, match):
        matches = [match for _round in self.tournament.rounds for match in _round.matches]
        for existing_match in matches:
            if match == existing_match:
                return True
        return False


class RoundController:
    def __init__(self, views, tournament):
        self.views = views
        self.storage = Storage('tournaments')
        self.tournament = tournament
        self.new_round = NewRound(views, tournament)
        self.round = self.tournament.rounds[-1] if self.tournament.rounds else None

    @property
    def title(self):
        return self.views.title_view

    @property
    def interface(self):
        return self.views.interface

    @property
    def report(self):
        return self.views.report

    @property
    def round_view(self):
        return self.views.round_view

    @property
    def error_view(self):
        return self.views.error_view

    def add_round(self):
        if self.round:
            if not self.round.end_date:
                self.error_view.round_not_finished()
                return None
        if self.tournament.curent_round < self.tournament.number_of_rounds:
            self.round = self.new_round.generate()
            self.storage.update(self.tournament)
        else:
            self.error_view.tournament_ended()

    def select_winner(self):
        if not self.round.end_date:
            for match in self.round.matches:
                if not match.winner:
                    players = [match.player_1, match.player_2]
                    self.round_view.prompt_for_winner(match)
                    self.report.display_all([match])
                    if isinstance(match.player_2, str):
                        match.winner = match.player_1
                    else:
                        response = self.round_view.select('winner')
                        if response in ["1", "2", "3"]:
                            if response == '3':
                                match.winner = players
                            else:
                                match.winner = players[int(response) - 1]
                            self.storage.update(self.tournament)
            if all([match.winner for match in self.round.matches]):
                self.round.end()
            self.storage.update(self.tournament)

    def manager(self):
        stay = True
        while stay:
            self.title.round_menu(self.tournament.curent_round)
            self.report.display_all([self.round])
            response = self.interface.display_interface("round")
            if response == "1":
                self.select_winner()
            if response == "2":
                self.add_round()
            if response == "9":
                stay = False
