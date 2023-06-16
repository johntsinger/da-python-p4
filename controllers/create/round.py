from random import shuffle
from models.round import Round
from models.match import Match


class NewRound:
    """Controller to create a new round"""
    def __init__(self, views, tournament):
        self.views = views
        self.tournament = tournament
        self.round = None
        self.match_pool = None

    def exempt_player(self, players_list, matches, players_in_match):
        """Set exempt player when the number of players is odd.
        Exempts the player with the lowest score if he has not already
        been exempted.

        params :
            - player_list (list) : list of players in this tournment
            - matches (list) : list of matches for this round
            - players_in_match (list) : list of players already paired
                                        in this round

        return :
            list of matches, list of players in match
        """
        for i in reversed(range(len(players_list))):
            if not self.already_exempt(players_list[i]):
                uuid = 0
                match = Match(uuid, players_list[i], "EXEMPT")
                match.winner = match.player_1
                matches.append(match)
                players_in_match.append(players_list[i])
                return matches, players_in_match

    def pairing(self, players_list, matches, players_in_match, reset=False):
        """Pairs players 2 by 2, with rules :
            - players sorted by score :
                - player 1 vs player 2, player 3 vs player 4, ...
            - minimal score gap
            - players cannot play twice in the same round
            - avoid identical matches

        params :
            - player_list (list) : list of players in this tournment
            - matches (list) : list of matches for this round
            - players_in_match (list) : list of players already paired
                                        in this round
            - reset (bool default = False) : a flag

        return :
            list of matches
        """
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
                            matches = self.pairing(
                                players_list, matches,
                                players_in_match, reset=True)
                            if len(matches) == len(players_list) / 2:
                                return matches
                            break
                        # if it still misses a match in the second attempt
                        # add the match even if it has already been played
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

    def get_matches(self, players_list):
        """Generate matches"""
        matches = []
        players_in_match = []
        if len(players_list) % 2 == 1:
            matches, players_in_match = self.exempt_player(
                players_list, matches, players_in_match)
        matches = self.pairing(players_list, matches, players_in_match)
        return matches

    def generate(self):
        """Generate a round"""
        # list of players who did not withdraw
        players_list = [player for player in self.tournament.players
                        if not player.withdrawal]
        self.tournament.curent_round += 1
        round_name = f'Round {self.tournament.curent_round}'
        self.round = Round(round_name)
        if self.tournament.curent_round == 1:
            # random shuffling of the player list in round 1
            shuffle(players_list)
            for match in self.get_matches(players_list):
                self.round.matches.append(match)
        else:
            # sort player by score, buchholz and cumulative for other rounds
            players_list.sort(
                key=lambda obj: (
                    obj.score,
                    obj.buchholz_score,
                    obj.cumulative_score
                ), reverse=True
            )
            for match in self.get_matches(players_list):
                self.round.matches.append(match)
        self.tournament.rounds.append(self.round)
        return self.round

    def match_exists(self, match):
        """Check if a given match exists"""
        matches = [match for round_ in self.tournament.rounds
                   for match in round_.matches]
        for existing_match in matches:
            if match == existing_match:
                return True
        return False

    def get_players_exempt(self):
        """Get the list of exempt players"""
        matches = [match for round_ in self.tournament.rounds
                   for match in round_.matches]
        players_exempt = []
        for match in matches:
            if match.player_2 == 'EXEMPT':
                players_exempt.append(match.player_1)
        return players_exempt

    def already_exempt(self, player):
        """Check if a given player is already exempts"""
        players_exempt = self.get_players_exempt()
        if player in players_exempt:
            return True
        return False
