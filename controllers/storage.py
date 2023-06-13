from pathlib import Path
from tinydb import TinyDB
from tinydb.storages import JSONStorage
from tinydb_serialization import SerializationMiddleware
from tinydb_serialization.serializers import DateTimeSerializer
from models.player import Player
from models.tournament import Tournament


class Storage:
    """TinyDb controller"""
    DATA_FOLDER = Path('data')
    CLASSES = {'players': Player, 'tournaments': Tournament}

    def __init__(self, name):
        self.name = name
        self.serialization = SerializationMiddleware(JSONStorage)
        self.serialization.register_serializer(
            DateTimeSerializer(), 'TinyDate')
        self.db = TinyDB(self.DATA_FOLDER / f'{self.name}.json',
                         create_dirs=True, storage=self.serialization,
                         indent=4)

    def all(self):
        """Return all elements in the json db deserialized"""
        return [self.CLASSES[self.name].from_dict(dictionary)
                for dictionary in self.db.all()]

    def get(self, **kwargs):
        """Search elements in the json db by key=value
        and return them deserialized
        """
        def predicate(obj, kwargs):
            for key, value in kwargs.items():
                if key not in obj or obj[key] != value:
                    return False
            return True

        return [
            self.CLASSES[self.name].from_dict(dictionary)
            for dictionary
            in self.db.search(lambda obj: predicate(obj, kwargs))
        ]

    def get_elt_by_id(self, uuid):
        """Search element in json db by id and return it deserialized"""
        dictionary = self.db.get(doc_id=uuid)
        return self.CLASSES[self.name].from_dict(dictionary)

    def update(self, obj):
        """Add serialized object to json db"""
        self.db.update(obj.cleaned_data, doc_ids=[obj.uuid])

    def remove(self, obj):
        """Remove object from json db"""
        self.db.remove(doc_ids=[obj.uuid])
