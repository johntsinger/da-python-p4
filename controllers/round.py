from controllers.storage import Storage
from controllers.create.round import NewRound
from models.exceptions import UserExitException
from utils.tools import clear_console


class RoundController:
    """Round menu controller"""
    def __init__(self, views, tournament, pretty_table):
        self.views = views
        self.pretty_table = pretty_table
        self.storage = Storage('tournaments')
        self.tournament = tournament
        self.new_round = NewRound(tournament)
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
        """Add a new round if tournament is not over"""
        if self.round:
            if not self.round.end_date:
                self.error_view.round_not_over()
                self.views.wait.wait()
                return None
        if self.tournament.curent_round < self.tournament.number_of_rounds:
            self.round = self.new_round.generate()
            self.storage.update(self.tournament)
        else:
            self.error_view.round_tournament_over()
            self.views.wait.wait()

    def select_match(self):
        matches = [match for match in self.round.matches if not match.winner]
        self.pretty_table.display(matches)
        response = self.round_view.select('match')
        if response in [str(match.uuid) for match in matches]:
            return next(match for match in matches
                        if match.uuid == int(response))
        elif response == 'q':
            raise UserExitException
        else:
            self.error_view.not_exist('round', response)
            self.views.wait.wait()

    def select_winner(self):
        if self.round.end_date:
            self.error_view.round_over()
            self.views.wait.wait()
        while not self.round.end_date:
            clear_console()
            self.title_view.round_menu(self.tournament.curent_round)
            try:
                match = self.select_match()
            except UserExitException:
                return None
            if match:
                self.set_winner(match)

    def set_winner(self, match):
        players = [match.player_1, match.player_2]
        self.round_view.prompt_for_winner(match)
        self.pretty_table.display([match])
        # if the player is exempted, he wins
        if isinstance(match.player_2, str):
            match.winner = match.player_1
            self.storage.update(self.tournament)
        else:
            response = self.round_view.select(
                'winner',
                [player.display_without_score() for player in players]
            )
            if response in ["1", "2", "3"]:
                # if the response is 3, it's a draw
                if response == '3':
                    match.winner = players
                    self.storage.update(self.tournament)
                # if the response is 1, player 1 win
                # if the response is 2, player 2 win
                else:
                    match.winner = players[int(response) - 1]
                    self.storage.update(self.tournament)
        if all([match.winner for match in self.round.matches]):
            self.round.end()
            self.add_cumulative_score()
            self.cumulative_score()
            self.buchholz_score()
            self.storage.update(self.tournament)

    def cumulative_score(self):
        """Calculate cumulative score for all players
        Cumulative tie-breaking system :
            sum the running score for each round
        """
        for player in self.tournament.players:
            cumulative_score = sum(player.cumulative_list)
            if isinstance(cumulative_score, float):
                if cumulative_score.is_integer():
                    cumulative_score = int(cumulative_score)
            player.cumulative_score = cumulative_score

    def add_cumulative_score(self):
        """After each round add in a list the actual score of the players
        to calculate the cumulative score"""
        for match in self.round.matches:
            match.player_1.cumulative_list.append(match.player_1.score)
            if not isinstance(match.player_2, str):
                match.player_2.cumulative_list.append(match.player_2.score)

    def get_opponents(self, player):
        """Get all opponents of a given player to calculate buchholz score"""
        opponents = []
        for round_ in self.tournament.rounds:
            for match in round_.matches:
                if player in match:
                    if player == match.player_1:
                        if not isinstance(match.player_2, str):
                            opponents.append(match.player_2)
                    else:
                        opponents.append(match.player_1)
        return opponents

    def buchholz_score(self):
        """Calculate the buchholz score for all players
        Buchholz tie-breaking system :
            sum the score of all a player's opponents
        """
        for player in self.tournament.players:
            opponents = self.get_opponents(player)
            buchholz_score = sum(
                [opponent.score for opponent in opponents])
            if isinstance(buchholz_score, float):
                if buchholz_score.is_integer():
                    buchholz_score = int(buchholz_score)
            player.buchholz_score = buchholz_score

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
