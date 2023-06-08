from pathlib import Path
from ansi2html import Ansi2HTMLConverter
from prettytable import PrettyTable
from prettytable import ALL
from datetime import datetime
from models.match import Match


class MyPrettyTable:
    # Color
    R = "\033[0;31;40m"  # RED
    G = "\033[0;32;40m"  # GREEN
    Y = "\033[0;33;40m"  # Yellow
    B = "\033[0;34;40m"  # Blue
    BL = "\033[38;5;75m"
    N = "\033[0m"  # Reset

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
        keys = []
        for key in vars(item).keys():
            if key == 'uuid':
                key = 'Id'
            key = key.lstrip("_").capitalize().replace('_', ' ')
            keys.append(key.upper())
        return keys

    def get_value(self, item):
        values = []
        for key, value in vars(item).items():
            if isinstance(value, datetime):
                if value.hour:
                    value = value.strftime('%d/%m/%y\n%H:%M')
                else:
                    value = value.strftime('%d/%m/%Y')
            elif not value:
                if key != 'score':
                    value = ""
            value = self.wrap_list(value)
            values.append(value)
        return values

    def match(self, items):
        self.table.clear()
        key = ['ID', 'PLAYER 1', 'PLAYER 2', 'WINNER']
        self.table.field_names = key
        for i, item in enumerate(items):
            self.table.add_row(
                [item.uuid, item.player_1.display_in_match(),
                 item.player_2.display_in_match(), item.winner]
            )

    def wrap_list(self, value):
        if isinstance(value, list):
            # sort players by score
            try:
                value.sort(key=lambda obj: obj.score, reverse=True)
            except AttributeError:
                pass
            string = ''
            for elt in value:
                string += f"{elt}\n"
            return string
        if isinstance(value, datetime):
            return value.strftime("%d/%m/%Y %H:%M")
        return value

    def get_table(self, items):
        self.table.clear()
        self.table.field_names = (self.get_key(items[0]))
        for item in items:
            self.table.add_row(self.get_value(item))
        if isinstance(items[0], Match):
            self.match(items)

        self.table.field_names = [
            self.BL+key+self.N for key in self.table.field_names
        ]

    def display(self, items):
        self.get_table(items)
        self.pretty_table_view.display(self.table)

    def to_html(self, items):
        self.get_table(items)
        table_html_string = self.table.get_html_string(
            format=True, border=True)
        to_html = Ansi2HTMLConverter(
            escaped=False, font_size='18px').convert(
            table_html_string, full=False)
        return to_html

    def write_html(self, name, to_html):
        path = Path('html-report')
        path.mkdir(parents=True, exist_ok=True)
        with open(path / (name + '.html'), 'w', encoding='utf-8') as file:
            file.write(to_html)

    def export_html(self, name, item):
        response = self.export_view.export()
        if response:
            to_html = self.to_html(item)
            self.write_html(name, to_html)
            self.export_view.export_confirmation(name)
