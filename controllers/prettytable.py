from pathlib import Path
from ansi2html import Ansi2HTMLConverter
from prettytable import PrettyTable
from prettytable import ALL
from datetime import datetime
from models.match import Match
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
            key = key.lstrip("_").capitalize().replace('_', ' ')
            keys.append(key.upper())
        return keys

    def get_value(self, item):
        """Extract attributes values of the item to create rows"""
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
        """Create PrettyTable for a Match"""
        self.table.clear()
        key = ['ID', 'PLAYER 1', 'PLAYER 2', 'WINNER']
        self.table.field_names = key
        for i, item in enumerate(items):
            self.table.add_row(
                [item.uuid, item.player_1.display_in_match(),
                 item.player_2.display_in_match(), item.winner
                 if item.winner else '']
            )

    def wrap_list(self, value):
        """Transform list value to string"""
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
        return value

    def get_table(self, items):
        """Add headers and rows in PrettyTable
        Ïf items are matches set a custom PrettyTable for matches

        params:
            - items : a list of instances to add in the PrettyTable
        """
        self.table.clear()
        if isinstance(items[0], Match):
            self.match(items)
        else:
            self.table.field_names = (self.get_key(items[0]))
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
