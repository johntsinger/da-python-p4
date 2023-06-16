from datetime import datetime
from models.match import Match


class Round:
    """Model for a round"""
    def __init__(self, name, start_date=None,
                 end_date=None, matches=None):
        self.name = name
        self.start_date = start_date if start_date else datetime.now()
        self.end_date = end_date
        self.matches = matches if matches else []

    @property
    def cleaned_data(self):
        """Serialize object"""
        dictionary = {}
        for key, value in vars(self).items():
            key = key.lstrip('_')
            if isinstance(value, list):
                dictionary[key] = [elt.cleaned_data for elt in value]
            else:
                dictionary[key] = value
        return dictionary

    @classmethod
    def from_dict(cls, dictionary, players):
        """Deserialize object"""
        for key, value in dictionary.items():
            if key == "matches":
                dictionary[key] = [
                    Match.from_dict(elt, players) for elt in value
                ]
        return cls(**dictionary)

    def end(self):
        """Set the end_date of a round"""
        self.end_date = datetime.now()

    def add_match(self, match):
        self.matches.append(match)

    def __str__(self):
        matches = ""
        for i, match in enumerate(self.matches):
            matches += f'Match {i + 1} : {match}\n'
        return f"{self.name:^55} \n{matches}"

    def __repr__(self):
        return str(self)
