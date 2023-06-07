from random import shuffle
from models.round import Round
from models.match import Match


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
        while i < len(players_list):
            uuid = len(matches) if len(players_list) % 2 else len(matches) + 1
            if not players_list[i] in players_in_match:
                j = i + 1
                while players_list[j] in players_in_match:
                    j += 1
                match = Match(uuid, players_list[i], players_list[j])
                while self.match_exists(match):
                    try:
                        j += 1
                        if players_list[j] in players_in_match:
                            continue
                        match = Match(uuid, players_list[i], players_list[j])
                    except IndexError:
                        # if first time index error try revert list
                        # and pairing again
                        if not reset:
                            players_list.sort(key=lambda obj: obj.score)
                            matches = self.pairing(players_list, reset=True)
                            if len(matches) == len(players_list) / 2:
                                return matches
                            break
                        # if it still misses a match add the match
                        # even if it has already been played
                        else:
                            players = [player for player in players_list
                                       if player not in players_in_match]
                            match = Match(uuid, players[0], players[1])
                            matches.append(match)
                            players_in_match.append(players[0])
                            players_in_match.append(players[1])
                            break
                else:
                    matches.append(match)
                    players_in_match.append(players_list[i])
                    players_in_match.append(players_list[j])
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
