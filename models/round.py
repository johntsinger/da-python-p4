from datetime import datetime
from models.match import Match


class Round:
    def __init__(self, name, start_date=datetime.now(),
                 end_date=None, matches=[]):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.matches = matches

    @property
    def cleaned_data(self):
        dictionary = {}
        for key, value in vars(self).items():
            key = key.lstrip('_')
            if isinstance(value, list):
                dictionary[key] = [elt.cleaned_data for elt in value]
            else:
                dictionary[key] = value
        return dictionary

    @classmethod
    def from_dict(cls, dictionary):
        for key, value in dictionary.items():
            if key == "matches":
                dictionary[key] = [Match.from_dict(elt) for elt in value]
        return Round(**dictionary)

    def end(self):
        self.end_date = datetime.now()

    def add_match(self, match):
        self.matches.append(match)

    def __str__(self):
        matches = ""
        for match in self.matches:
            matches += f'{match}\n'
        return f"{self.name} :\n{matches}"

    def __repr__(self):
        return str(self)
