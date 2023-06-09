from controllers.storage import Storage
from models.exceptions import UserExitException
from controllers.create.player import NewPlayer
from utils.tools import clear_console


class PlayerMenu:
    """Player menu controller"""
    def __init__(self, views, pretty_table):
        self.views = views
        self.pretty_table = pretty_table
        self.storage = Storage('players')
        self.create_player = NewPlayer(views, self.storage.all())
        self.player = None

    @property
    def interface_view(self):
        return self.views.interface

    @property
    def create_view(self):
        return self.views.create

    @property
    def title_view(self):
        return self.views.title

    @property
    def player_view(self):
        return self.views.player

    @property
    def error_view(self):
        return self.views.error

    def new_player(self):
        self.title_view.new_player()
        try:
            new_player = self.create_player.create()
        except UserExitException:
            return None
        if new_player:
            if self.create_view.accept("player", new_player):
                new_player.uuid = self.storage.db.insert(
                    new_player.cleaned_data)
                self.storage.update(new_player)

    def export_all_players(self):
        self.title_view.export_players()
        players = self.storage.all()
        if players:
            players.sort(key=lambda obj: (obj.last_name, obj.first_name))
            self.player_view.players_sort_info()
            self.pretty_table.display(players)
            self.pretty_table.export_html('players', players)
        else:
            self.error_view.nothing_to_display('player')
        self.views.wait.wait()

    def select_player(self):
        players = self.storage.all()
        if players:
            players.sort(key=lambda obj: (obj.last_name, obj.first_name))
            self.pretty_table.display(players)
            response = self.player_view.select('player')
            if response in [str(player.uuid)
                            for player in players]:
                return self.storage.get_elt_by_id(int(response))
        return None

    def delete_player(self):
        self.title_view.delete_player()
        player = self.select_player()
        if player:
            response = self.player_view.accept_delete(player)
            if response:
                self.storage.remove(player)
        # if no player in json db
        elif not self.storage.db.all():
            self.error_view.nothing_to_display('player')
            self.views.wait.wait()

    def manager(self):
        stay = True
        while stay:
            clear_console()
            self.title_view.player_menu()
            response = self.interface_view.display_interface('player')
            if response == '1':
                clear_console()
                self.new_player()
            elif response == '2':
                clear_console()
                self.export_all_players()
            elif response == '6':
                clear_console()
                self.delete_player()
            elif response == '9':
                stay = False
