from random import shuffle
from models.round import Round
from models.match import Match
from models.storage import Storage


class NewRound:
    def __init__(self, views, tournament):
        self.views = views
        self.tournament = tournament
        self.round = None
        self.match_pool = None

    @property
    def round_view(self):
        return self.views.round_view

    @property
    def report(self):
        return self.views.report

    def pairing(self, players_list):
        matches = []
        players_in_match = []
        if len(players_list) % 2 == 1:
            for i in reversed(range(len(players_list))):
                if not self.already_exempt(players_list[i]):
                    uuid = len(matches) + 1
                    matches.append(Match(uuid, players_list[i], "EXEMPT"))
                    players_in_match.append(players_list[i])
                    break

        i = 0
        print(len(players_list))
        while i < len(players_list):
            print(players_in_match)
            uuid = len(matches) + 1
            if not players_list[i] in players_in_match:
                j = i + 1
                while players_list[j] in players_in_match:
                    j += 1
                match = Match(uuid, players_list[i], players_list[j])
                print('ici : ', match)
                while self.match_exists(match):
                    try:
                        j += 1
                        if players_list[j] in players_in_match:
                            continue
                        match = Match(uuid, players_list[i], players_list[j])
                    except IndexError:
                        break
                else:
                    print("used : ", match)
                    self.views.wait.wait()
                    matches.append(match)
                    players_in_match.append(players_list[i])
                    players_in_match.append(players_list[j])
                    print(matches)
            i += 1
        return matches

    def generate(self):
        players_list = list(self.tournament.players)
        self.tournament.curent_round += 1
        round_name = f'Round {self.tournament.curent_round}'
        self.round = Round(round_name)
        if self.tournament.curent_round == 1:
            shuffle(players_list)
            for match in self.pairing(players_list):
                self.round.matches.append(match)
        else:
            players_list.sort(key=lambda obj: obj.score, reverse=True)
            for match in self.pairing(players_list):
                self.round.matches.append(match)
        self.tournament.rounds.append(self.round)
        return self.round

    def match_exists(self, match):
        matches = [match for _round in self.tournament.rounds
                   for match in _round.matches]
        for existing_match in matches:
            if match == existing_match:
                return True
        return False

    def get_players_exempt(self):
        matches = [match for _round in self.tournament.rounds
                   for match in _round.matches]
        players_exempt = []
        for match in matches:
            if match.player_2 == 'EXEMPT':
                players_exempt.append(match.player_1)
        return players_exempt

    def already_exempt(self, player):
        players_exempt = self.get_players_exempt()
        if player in players_exempt:
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
                self.error_view.round_not_over()
                return None
        if self.tournament.curent_round < self.tournament.number_of_rounds:
            self.round = self.new_round.generate()
            self.storage.update(self.tournament)
        else:
            self.error_view.tournament_over()

    def select_match(self):
        matches = [match for match in self.round.matches if not match.winner]
        self.report.display_all(matches)
        response = self.round_view.select('match')
        if response in [str(match.uuid) for match in matches]:
            return next(match for match in matches if match.uuid == int(response))

    def select_winner(self):
        while not self.round.end_date:
            match = self.select_match()
            if match:
                players = [match.player_1, match.player_2]
                self.round_view.prompt_for_winner(match)
                self.report.display_all([match])
                if isinstance(match.player_2, str):
                    match.winner = match.player_1
                    self.storage.update(self.tournament)
                else:
                    response = self.round_view.select('winner')
                    if response in ["1", "2", "3"]:
                        if response == '3':
                            match.winner = players
                            self.storage.update(self.tournament)
                        else:
                            match.winner = players[int(response) - 1]
                            self.storage.update(self.tournament)
                        
                if all([match.winner for match in self.round.matches]):
                    self.round.end()
                self.storage.update(self.tournament)
        else:
            self.error_view.round_over()

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
