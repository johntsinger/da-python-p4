from pathlib import Path
from ansi2html import Ansi2HTMLConverter
from prettytable import PrettyTable
from prettytable import ALL
from datetime import datetime
from models.match import Match
from models.tournament import Tournament
from models.player import PlayerInTournament
from utils.ansi_colors import BL, N


class MyPrettyTable:
    """Controller to display PrettyTable"""
    def __init__(self, views):
        self.views = views
        self.table = PrettyTable(hrules=ALL, padding_width=1)
        self.table.align = 'l'

    @property
    def pretty_table_view(self):
        return self.views.pretty_table

    @property
    def export_view(self):
        return self.views.export

    def get_key(self, item):
        """Extract attributes names of the item to create headers"""
        keys = []
        for key in vars(item).keys():
            if key == 'uuid':
                key = 'Id'
            # don't display cumulative list
            elif key == 'cumulative_list':
                continue
            key = key.lstrip("_").capitalize().replace('_', ' ')
            keys.append(key.upper())
        return keys

    def get_value(self, item):
        """Extract attributes values of the item to create rows"""
        values = []
        for key, value in vars(item).items():
            # don't display cumulative list
            if key == "cumulative_list":
                continue
            if isinstance(value, datetime):
                if value.hour:
                    value = value.strftime('%d/%m/%y\n%H:%M')
                else:
                    value = value.strftime('%d/%m/%Y')
            elif not value:
                if key not in ('score', 'buchholz_score', 'cumulative_score'):
                    value = ""
            value = self.wrap_list(value)
            values.append(value)
        return values

    def match(self, items):
        """Create PrettyTable for a Match"""
        self.table.clear()
        key = ['ID', 'PLAYER 1', 'PLAYER 2', 'WINNER']
        self.table.field_names = key
        for i, item in enumerate(items):
            self.table.add_row(
                [item.uuid, item.player_1.display_without_score(),
                 item.player_2.display_without_score(), item.winner
                 if item.winner else '']
            )

    def tournament(self, items):
        """Add rows for a tournament : first add tournaments in progress,
        add a divider, then add tournaments that have ended
        """
        tournaments = [
            item for item in items
            if item.curent_round != item.number_of_rounds
        ]
        tournaments_over = [
            item for item in items
            if item.curent_round == item.number_of_rounds
        ]
        for i, tournament in enumerate(tournaments):
            # add a divider for the last tournament in progress
            if i == len(tournaments) - 1:
                self.table.add_row(
                    self.get_value(tournament),
                    divider=True
                )
            else:
                self.table.add_row(self.get_value(tournament))
        for tournament in tournaments_over:
            self.table.add_row(self.get_value(tournament))

    def wrap_list(self, value):
        """Transform list value to string"""
        if isinstance(value, list):
            # sort players by score, buchholz and cumulative
            try:
                value.sort(
                    key=lambda obj: (
                        obj.score,
                        obj.buchholz_score,
                        obj.cumulative_score
                    ), reverse=True
                )
            except AttributeError:
                pass
            string = ''
            rank = 1
            for i, elt in enumerate(value):
                if value:
                    # set rank if value is a list of player in tournament
                    # this list can only be found in a tournament
                    if isinstance(value[0], PlayerInTournament):
                        rank = self.get_rank(value, i, rank)
                        # add a space if rank < 10 to maintain alignment
                        if rank < 10:
                            string += f"{rank}.  {elt}\n"
                        else:
                            string += f"{rank}. {elt}\n"
                    else:
                        string += f"{elt}\n"
            return string
        return value

    def get_rank(self, value, index, rank):
        """Get the rank to display it in a tournament

        params:
            - value (list) : list of PlayerInTournament instance
            - index (int) : the index of the list
            - rank (int) : the rank of the previous player
        return:
            - rank (int) : the rank of the player tested
        """
        if index:
            player = value[index]
            previous_player = value[index - 1] 
            if ((player.score,
                player.buchholz_score,
                player.cumulative_score) 
                == (previous_player.score,
                    previous_player.buchholz_score,
                    previous_player.cumulative_score)):
                return rank
            return index + 1  # to keep counting after a draw (i.e. 1, 1, 3)
        return rank

    def get_table(self, items):
        """Add headers and rows in PrettyTable
        Ïf items are matches set a custom PrettyTable for matches

        params:
            - items : a list of instances to add in the PrettyTable
        """
        self.table.clear()
        # If the item is a match set custom display
        if isinstance(items[0], Match):
            self.match(items)
        else:
            self.table.field_names = (self.get_key(items[0]))
            # If the item is a tournament, first add tournaments in progress,
            # then tournaments that have ended.
            if isinstance(items[0], Tournament):
                self.tournament(items)
            else:
                for item in items:
                    self.table.add_row(self.get_value(item))

        self.table.field_names = [
            BL+key+N for key in self.table.field_names
        ]

    def display(self, items):
        self.get_table(items)
        self.pretty_table_view.display(self.table)

    def to_html(self, items):
        """Tranform PrettyTable to HTML string

        params:
            - items : a list of instances to add in the PrettyTable
        """
        self.get_table(items)
        html_string = self.table.get_html_string(
            format=True, border=True)
        return html_string

    def convert_ansi_to_html(self, html_string):
        """Convert text with ANSI color codes to HTML
        params:
            - html_string (str) : an html representation of the table
                                  in string form
        """
        return Ansi2HTMLConverter(
            escaped=False, font_size='18px').convert(
            html_string, full=False)

    def write_html(self, name, html_string):
        """Write the HTML file

        params:
            - name (str) : the name of the file to save
            - html_string (str) : an html representation of the table
                                  in string form
        """
        path = Path('html-report')
        path.mkdir(parents=True, exist_ok=True)
        with open(path / (name + '.html'), 'w', encoding='utf-8') as file:
            file.write(html_string)

    def export_html(self, name, items):
        """Export the report

        params:
            - name (str) : the name of the file to save
            - items (list) : a list of instances to add in the PrettyTable
        """
        response = self.export_view.export()
        if response:
            to_html = self.to_html(items)
            to_html_converted = self.convert_ansi_to_html(to_html)
            self.write_html(name, to_html_converted)
            self.export_view.export_confirmation(name)
