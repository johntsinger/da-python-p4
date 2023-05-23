from prettytable import PrettyTable
from prettytable import ALL
from datetime import datetime
from models.player import PlayerInTournament


class Report:
    def __init__(self):
        self.table = PrettyTable(hrules=ALL)

    def get_key(self, item):
        keys = []
        for key in vars(item).keys():
            if key == 'uuid':
                key = 'Id'
            key = key.lstrip("_").capitalize().replace('_', ' ')
            keys.append(key)
        return keys

    def get_value(self, item):
        values = []
        for value in vars(item).values():
            if isinstance(value, datetime):
                if value.hour:
                    value = value.strftime('%d/%m/%y\n%H:%M')
                else:
                    value = value.strftime('%d/%m/%Y')
            value = self.wrap_list(value)
            values.append(value)
        return values

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

    def display_all(self, items):
        self.table.clear()
        """
        self.table.field_names = [
            key.lstrip('_').capitalize().replace('_', ' ')
            for key in vars(items[0]).keys()
        ]
        """
        self.table.field_names = (self.get_key(items[0]))
        self.table.align = 'l'
        #self.table.header = False
        #self.table.add_row(self.get_key(items[0]))
        for item in items:
            """
            self.table.add_row(
                [self.wrap_list(value) for value in vars(item).values()])
            """
            self.table.add_row(self.get_value(item))

        print(self.table)
        print()