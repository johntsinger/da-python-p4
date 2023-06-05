from random import shuffle
from models.round import Round
from models.match import Match
from models.storage import Storage
from utils.tools import clear_console


class NewRound:
    def __init__(self, views, tournament):
        self.views = views
        self.tournament = tournament
        self.round = None
        self.match_pool = None

    def pairing(self, players_list, reset=False):
        matches = []
        players_in_match = []
        if len(players_list) % 2 == 1:
            for i in reversed(range(len(players_list))):
                if not self.already_exempt(players_list[i]):
                    uuid = 0
                    match = Match(uuid, players_list[i], "EXEMPT")
                    match.winner = match.player_1
                    matches.append(match)
                    players_in_match.append(players_list[i])
                    break

        i = 0
        print(len(players_list))
        while i < len(players_list):
            print(players_in_match)
            uuid = len(matches) if len(players_list) % 2 else len(matches) + 1
            if not players_list[i] in players_in_match:
                j = i + 1
                while players_list[j] in players_in_match:
                    j += 1
                    print('première boucle j', j)
                match = Match(uuid, players_list[i], players_list[j])
                print('ici : ', match)
                while self.match_exists(match):
                    try:
                        j += 1
                        print('deuxieme boucle j', j)
                        if players_list[j] in players_in_match:
                            continue
                        match = Match(uuid, players_list[i], players_list[j])
                    except IndexError:
                        print('INDEX ERROR')
                        print(i, j)
                        # if first time index error try revert list
                        # and pairing again
                        print('reset', reset)
                        if not reset:
                            print('2e FONCTONS')
                            players_list.sort(key=lambda obj: obj.score)
                            print('PLAYER LIST : ', players_list)
                            matches = self.pairing(players_list, reset=True)
                            if len(matches) == len(players_list) / 2:
                                return matches
                            break
                        # if it still misses a match add the match 
                        # even if it has already been played
                        else:
                            print("Not working")
                            players = [player for player in players_list 
                                       if player not in players_in_match]
                            print(players)
                            match = Match(uuid, players[0], players[1])
                            print(matches)
                            matches.append(match)
                            print(matches)
                            players_in_match.append(players[0])
                            players_in_match.append(players[1])
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
    def __init__(self, views, tournament, pretty_table):
        self.views = views
        self.pretty_table = pretty_table
        self.storage = Storage('tournaments')
        self.tournament = tournament
        self.new_round = NewRound(views, tournament)
        self.round = self.tournament.rounds[
            -1] if self.tournament.rounds else None

    @property
    def title_view(self):
        return self.views.title

    @property
    def interface_view(self):
        return self.views.interface

    @property
    def round_view(self):
        return self.views.round

    @property
    def error_view(self):
        return self.views.error

    def add_round(self):
        if self.round:
            if not self.round.end_date:
                self.error_view.round_not_over()
                self.views.wait.wait()
                return None
        if self.tournament.curent_round < self.tournament.number_of_rounds:
            self.round = self.new_round.generate()
            self.storage.update(self.tournament)
        else:
            self.error_view.tournament_over()
            self.views.wait.wait()

    def select_match(self):
        matches = [match for match in self.round.matches if not match.winner]
        self.pretty_table.display(matches)
        response = self.round_view.select('match')
        if response in [str(match.uuid) for match in matches]:
            return next(match for match in matches
                        if match.uuid == int(response))
        elif response == 'q':
            return None

    def select_winner(self):
        if self.round.end_date:
            self.error_view.round_over()
            self.views.wait.wait()
        while not self.round.end_date:
            clear_console()
            self.title_view.round_menu(self.tournament.curent_round)
            match = self.select_match()
            if match:
                players = [match.player_1, match.player_2]
                self.round_view.prompt_for_winner(match)
                self.pretty_table.display([match])
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
                return None

    def manager(self):
        stay = True
        while stay:
            clear_console()
            self.title_view.round_menu(self.tournament.curent_round)
            self.pretty_table.display([self.round])
            response = self.interface_view.display_interface("round")
            if response == "1":
                self.select_winner()
            elif response == "2":
                self.add_round()
            elif response == "9":
                stay = False
