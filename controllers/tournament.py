from controllers.storage import Storage
from models.player import PlayerInTournament
from models.exceptions import UserExitException
from controllers.create.tournament import NewTournament
from controllers.round import RoundController
from utils.tools import clear_console
import dateutil.parser
from dateutil.parser import ParserError


class TournamentsMenu:
    """Tournaments menu controller"""
    def __init__(self, views, pretty_table):
        self.views = views
        self.pretty_table = pretty_table
        self.storage = Storage('tournaments')
        self.create_tournament = NewTournament(
            self.views, self.storage.all(), self.pretty_table)
        self.tournament_controller = TournamentController(
            self.views, self.pretty_table)

    @property
    def interface_view(self):
        return self.views.interface

    @property
    def create_view(self):
        return self.views.create

    @property
    def tournament_view(self):
        return self.views.tournament

    @property
    def title_view(self):
        return self.views.title

    @property
    def error_view(self):
        return self.views.error

    def new_tournament(self):
        self.title_view.new_tournament()
        new_tournament = None
        # Exception raised if user type 'q' during creation
        try:
            new_tournament = self.create_tournament.create()
        except UserExitException:
            return None
        if new_tournament:
            if self.create_view.accept("tournament", new_tournament):
                new_tournament.uuid = self.storage.db.insert(
                    new_tournament.cleaned_data)
                self.storage.update(new_tournament)

    def select_tournament(self):
        tournaments = self.storage.all()
        if tournaments:
            self.tournament_view.short_form_info()
            self.pretty_table.display(tournaments)
            response = self.tournament_view.select('tournament')
            if response not in [str(tournament.uuid)
                                for tournament in tournaments]:
                return None
            if response:
                return self.storage.get_elt_by_id(int(response))
        return None

    def access_tournament(self):
        self.title_view.select_tournament()
        tournament = self.select_tournament()
        if tournament:
            self.tournament_controller.tournament = tournament
            self.tournament_controller.get_players_list()
            self.tournament_controller.manager()
        elif not self.storage.db.all():
            self.error_view.nothing_to_display('tournament')
            self.views.wait.wait()

    def delete_tournament(self):
        self.title_view.delete_tournament()
        tournament = self.select_tournament()
        if tournament:
            response = self.tournament_view.accept_delete(
                'tournament', tournament)
            if response:
                self.storage.remove(tournament)
                # update the list of tournament instances in the
                # NewTournament controller
                self.create_tournament.instances = self.storage.all()
        elif not self.storage.db.all():
            self.error_view.nothing_to_display('tournament')
            self.views.wait.wait()

    def get_tournament(self):
        """Get the tournament corresponding to the given name and start date"""
        tournaments = self.storage.all()
        if tournaments:
            name = self.tournament_view.prompt_for('Name')
            date = self.tournament_view.prompt_for('Start date')
            try:
                date = dateutil.parser.parse(
                    date, dayfirst=True).strftime('%d/%m/%Y %H:%M')
            except ParserError:
                date = None
            result = None
            for tournament in tournaments:
                if (tournament.name == name.capitalize()
                        and tournament.start_date == date):
                    result = tournament
            if result:
                return result
            else:
                self.error_view.no_tournament_found(name.capitalize(), date)
                self.views.wait.wait()
        else:
            self.error_view.nothing_to_display('tournament')
            self.views.wait.wait()

    def search_tournament(self):
        """Access the tournament found by it's name and start date"""
        self.title_view.search_tournament()
        self.tournament_view.search_info()
        tournament = self.get_tournament()
        if tournament:
            self.tournament_controller.tournament = tournament
            self.tournament_controller.get_players_list()
            self.tournament_controller.manager()

    def export_all_tournaments(self):
        self.title_view.export_all_tournaments()
        tournaments = self.storage.all()
        if tournaments:
            self.tournament_view.short_form_info()
            self.pretty_table.display(tournaments)
            self.pretty_table.export_html('tournaments', tournaments)
        else:
            self.error_view.nothing_to_display('tournament')
        self.views.wait.wait()

    def manager(self):
        stay = True
        while stay:
            clear_console()
            self.title_view.tournaments_menu()
            response = self.interface_view.display_interface('tournament')
            if response == '1':
                clear_console()
                self.new_tournament()
            elif response == '2':
                clear_console()
                self.access_tournament()
            elif response == '3':
                clear_console()
                self.search_tournament()
            elif response == '4':
                clear_console()
                self.export_all_tournaments()
            elif response == '6':
                clear_console()
                self.delete_tournament()
            elif response == '9':
                stay = False


class TournamentController:
    """Tournament menu controller"""
    def __init__(self, views, pretty_table):
        self.views = views
        self.pretty_table = pretty_table
        self.storage = Storage('tournaments')
        self._tournament = None
        self.round_controller = None
        self.players_list = None

    @property
    def interface_view(self):
        return self.views.interface

    @property
    def title_view(self):
        return self.views.title

    @property
    def tournament_view(self):
        return self.views.tournament

    @property
    def error_view(self):
        return self.views.error

    @property
    def tournament(self):
        return self._tournament

    @tournament.setter
    def tournament(self, value):
        """Set round controller when tournament is set"""
        self._tournament = value
        self.round_controller = RoundController(
            self.views, self._tournament, self.pretty_table)

    def start(self):
        """Start or continue tournament"""
        if len(self.tournament.players) < 2:
            self.title_view.round_menu('#')
            self.error_view.player_required()
            self.views.wait.wait()
            return None
        if not self.tournament.rounds:
            self.adjust_number_of_round()
            self.round_controller.add_round()
        self.round_controller.manager()

    def max_round(self):
        """Check the maximun number of round that can be played"""
        number_of_players = len(self.tournament.players)
        if number_of_players % 2:
            return number_of_players
        return number_of_players - 1

    def adjust_number_of_round(self):
        max_round = self.max_round()
        if self.tournament.number_of_rounds > max_round:
            self.error_view.wrong_number_of_round(
                self.tournament.number_of_rounds,
                max_round
            )
            self.tournament.number_of_rounds = max_round
            self.views.wait.wait()

    def add_player(self):
        """Add player to this tournament"""
        self.title_view.add_players()
        # check if there are players in json db
        if not Storage('players').db.all():
            self.error_view.nothing_to_display('player')
            self.views.wait.wait()
        else:
            if not self.tournament.rounds:
                keep_selecting = True
                while self.players_list and keep_selecting:
                    player = self.select_player(
                        self.players_list, add_player=True)
                    if player:
                        if player == 'q':
                            keep_selecting = False
                        else:
                            player_in_tournament = \
                                self.to_player_in_tournament(
                                    player)
                            self.tournament_view.display_player(player)
                            self.tournament.add_player(player_in_tournament)
                            self.storage.update(self.tournament)
                if not self.players_list:
                    self.error_view.all_players_added()
                    self.views.wait.wait()
            else:
                self.error_view.tournament_has_started()
                self.views.wait.wait()

    def delete_player(self):
        """Removes the player from the tournament if the tournament has not
        started, otherwise keeps the player in the tournament and do
        a player withdrawal
        """
        self.title_view.delete_player()
        if self.tournament.players:
            if self.tournament.curent_round < self.tournament.number_of_rounds:
                players_list = [player for player in self.tournament.players
                                if not player.withdrawal]
                player = self.select_player(players_list)
                self.title_view.delete_player()
                if player:
                    response = self.tournament_view.accept_delete(
                        'player', player)
                    if response:
                        # remove the player if match has not started
                        if not self.tournament.rounds:
                            self.tournament.remove_player(player)
                        else:
                            # don't remove it but set withdrawal
                            # and not play again
                            player.withdrawal = True
                            self.update_round()
                        self.are_enough_players()
                        self.storage.update(self.tournament)
                        # update self.players_list
                        self.get_players_list()
            else:
                self.error_view.tournament_over()
                self.views.wait.wait()
        else:
            self.error_view.nothing_to_display('player')
            self.views.wait.wait()

    def are_enough_players(self):
        """Check if there are enough players to continue the tournament.
        If not end the tournament
        """
        players_list = [player for player in self.tournament.players
                        if not player.withdrawal]
        if len(players_list) < 2 and self.tournament.rounds:
            self.error_view.not_enough_player()
            # end the tournament
            self.tournament.number_of_rounds = self.tournament.curent_round
            self.tournament.rounds[-1].end()
            self.views.wait.wait()

    def update_round(self):
        """Update round after player withdrawal"""
        for match in self.tournament.rounds[-1].matches:
            if not match.winner:
                if match.player_1.withdrawal:
                    match.winner = match.player_2
                elif match.player_2.withdrawal:
                    match.winner = match.player_1
        self.storage.update(self.tournament)

    def get_players_list(self):
        """Get the list of players not registered in this tournament"""
        storage = Storage('players').all()
        set1 = set(player_in_tournament.uuid for player_in_tournament
                   in self.tournament.players)
        self.players_list = [
            player for player in storage if player.uuid not in set1
        ]

    def select_player(self, players_list, add_player=False):
        """Select a player in a list of players

        Params:
            - players_list (list) : a list of players
              (can be self.players_list or self.tournament.players)
            - add_player (bool dafault=False) : a flag True if the caller is
              add_player
        Return:
            - a player (Player or PlayerInTournament)
        """
        players_list.sort(key=lambda obj: (obj.last_name, obj.first_name))
        self.pretty_table.display(players_list)
        response = self.tournament_view.select('player', to_stop=True)
        clear_console()
        # needed to display error under the title in add_player
        if add_player:
            self.title_view.add_players()
        if response == 'q':
            # don't return q to delete a player
            return response if add_player else None
        elif response in [str(player.uuid)
                          for player in players_list]:
            for player in players_list:
                # not use players_list[int(response) - 1] because uuids may not
                # follow each other if the object is deleted
                # (i.e. : 1, 3 if 2 has been deleted)
                if player.uuid == int(response):
                    return player
        self.error_view.not_exist('player', response)
        return None

    def to_player_in_tournament(self, player):
        """Transform Player to PlayerInTournament"""
        self.players_list.remove(player)
        return PlayerInTournament(player.last_name,
                                  player.first_name,
                                  player.date_of_birth,
                                  player.uuid)

    def date_isoformat(self):
        """Get date in iso format"""
        date = dateutil.parser.parse(self.tournament.start_date)
        return date.isoformat().replace(':', '')

    def export_players(self):
        self.title_view.export_players()
        self.tournament_view.players_sort_info()
        players = self.tournament.players
        if players:
            players.sort(key=lambda obj: (obj.last_name, obj.first_name))
            self.pretty_table.display(players)
            date_iso = self.date_isoformat()
            self.pretty_table.export_html(
                (f'players_in_tournament_{self.tournament.name}'
                 f'_{self.tournament.location}_{date_iso}'),
                players
            )
        else:
            self.error_view.nothing_to_display('player')
        self.views.wait.wait()

    def export_rounds(self):
        self.title_view.rounds_list()
        if self.tournament.rounds:
            self.pretty_table.display(self.tournament.rounds)
            date_iso = self.date_isoformat()
            self.pretty_table.export_html(
                (f'rounds_{self.tournament.name}_{self.tournament.location}'
                 f'_{date_iso}'),
                self.tournament.rounds
            )
        else:
            self.error_view.nothing_to_display('round')
        self.views.wait.wait()

    def export_this_tournament(self):
        self.title_view.export_tournament()
        self.tournament_view.short_form_info()
        self.pretty_table.display([self.tournament])
        date_iso = self.date_isoformat()
        self.pretty_table.export_html(
            (f'tournament_{self.tournament.name}_{self.tournament.location}'
             f'_{date_iso}'),
            [self.tournament]
        )
        self.views.wait.wait()

    def manager(self):
        stay = True
        while stay:
            clear_console()
            self.title_view.tournament_menu()
            self.tournament_view.short_form_info()
            self.tournament_view.tie_breaking_info()
            self.pretty_table.display([self.tournament])
            response = self.interface_view.display_interface('tournament_menu')
            if response == '1':
                clear_console()
                self.add_player()
            elif response == '2':
                clear_console()
                self.start()
            elif response == '3':
                clear_console()
                self.export_players()
            elif response == '4':
                clear_console()
                self.export_rounds()
            elif response == '5':
                clear_console()
                self.export_this_tournament()
            elif response == '6':
                clear_console()
                self.delete_player()
            elif response == '9':
                stay = False
