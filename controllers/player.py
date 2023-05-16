from models.storage import Storage
from controllers.create import NewPlayer
from utils.tools import clear_console


class PlayerMenu:
    def __init__(self, views):
        self.views = views
        self.storage = Storage('players')
        self.create_player = NewPlayer(views, self.storage.all())
        self.player = None

    @property
    def create_view(self):
        return self.views.create_view

    @property
    def title(self):
        return self.views.title_view

    @property
    def player_menu(self):
        return self.views.player_menu

    @property
    def report(self):
        return self.views.report

    def new_player(self):
        self.title.new_player_title()
        new_player = self.create_player.create()
        if new_player:
            if self.create_view.accept("player", new_player):
                new_player.uuid = self.storage.db.insert(
                    new_player.cleaned_data)
                self.storage.update(new_player)

    def display_all(self):
        players = self.storage.all()
        if players:
            players.sort(key=lambda obj: obj.last_name)
            self.report.display_all(players)
            self.views.wait.wait()

    def select_player(self):
        players = self.storage.all()
        if players:
            self.report.display_all(players)
            response = self.player_menu.select('player')
            if response not in [str(player.uuid)
                                for player in players]:
                return None
            if response:
                self.views.wait.wait()
                return self.storage.all()[int(response) - 1]
        return None

    def manager(self):
        stay = True
        while stay:
            clear_console()
            self.title.player_menu()
            response = self.player_menu.display_interface()
            if response == '0':
                clear_console()
                self.new_player()
            if response == '1':
                clear_console()
                self.display_all()
            if response == '6':
                player = self.select_player()
                if player:
                    self.storage.remove(player)
            if response == '9':
                stay = False