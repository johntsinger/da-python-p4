from models.storage import Storage
from models.exceptions import UserExitException
from controllers.create import NewPlayer
from utils.tools import clear_console


class PlayerMenu:
    def __init__(self, views, pretty_table):
        self.views = views
        self.pretty_table = pretty_table
        self.storage = Storage('players')
        self.create_player = NewPlayer(views, self.storage.all())
        self.player = None

    @property
    def interface(self):
        return self.views.interface

    @property
    def create_view(self):
        return self.views.create_view

    @property
    def title(self):
        return self.views.title_view

    @property
    def player_menu(self):
        return self.views.player_menu

    def new_player(self):
        self.title.new_player_title()
        try:
            new_player = self.create_player.create()
        except UserExitException:
            return None
        if new_player:
            if self.create_view.accept("player", new_player):
                new_player.uuid = self.storage.db.insert(
                    new_player.cleaned_data)
                self.storage.update(new_player)

    def display_all(self):
        self.title.players_list()
        players = self.storage.all()
        if players:
            players.sort(key=lambda obj: (obj.last_name, obj.first_name))
            self.pretty_table.display(players)
            self.views.wait.wait()

    def select_player(self):
        players = self.storage.all()
        if players:
            self.pretty_table.display(players)
            response = self.player_menu.select('player')
            if response not in [str(player.uuid)
                                for player in players]:
                return None
            if response:
                return self.storage.get_elt_by_id(int(response))
        return None

    def delete_player(self):
        self.title.delete_player()
        player = self.select_player()
        if player:
            self.storage.remove(player)

    def manager(self):
        stay = True
        while stay:
            clear_console()
            self.title.player_menu()
            response = self.interface.display_interface('player')
            if response == '1':
                clear_console()
                self.new_player()
            elif response == '2':
                clear_console()
                self.display_all()
            elif response == '6':
                clear_console()
                self.delete_player()
            elif response == '9':
                stay = False
