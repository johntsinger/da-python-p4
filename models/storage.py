import json
from pathlib import Path
from tinydb import TinyDB
from tinydb.storages import JSONStorage
from tinydb_serialization import SerializationMiddleware, Serializer
from tinydb_serialization.serializers import DateTimeSerializer
from models.player import Player, PlayerInTournament
from models.round import Round
from models.match import Match
from models.tournament import Tournament


class TournamentSerializer(Serializer):
    OBJ_CLASS = Tournament

    def encode(self, obj):
        return json.dumps(obj.cleaned_data)

    def decode(self, s):
        dictionary = json.loads(s)
        return Tournament.from_dict(dictionary)


class PlayerInTournamentSerializer(Serializer):
    OBJ_CLASS = PlayerInTournament

    def encode(self, obj):
        return json.dumps(obj.cleaned_data)

    def decode(self, s):
        dictionary = json.loads(s)
        return PlayerInTournament(**dictionary)


class RoundSerializer(Serializer):
    OBJ_CLASS = Round

    def encode(self, obj):
        return json.dumps(obj.cleaned_data)

    def decode(self, s):
        dictionary = json.loads(s)
        return Round.from_dict(dictionary)


class MatchSerializer(Serializer):
    OBJ_CLASS = Match

    def encode(self, obj):
        return json.dumps(obj.cleaned_data)

    def decode(self, s):
        dictionary = json.loads(s)
        return Match.from_dict(dictionary)


class PlayerSerializer(Serializer):
    OBJ_CLASS = Player

    def encode(self, obj):
        return json.dumps(obj.cleaned_data)

    def decode(self, s):
        dictionary = json.loads(s)
        return Player.from_dict(dictionary)


class Storage:
    DATA_FOLDER = Path('data')
    CLASSES = {'players': Player, 'tournaments': Tournament}

    def __init__(self, name):
        self.name = name
        self.serialization = SerializationMiddleware(JSONStorage)
        # self.serialization.register_serializer(MatchSerializer(), 'Match')
        # self.serialization.register_serializer(RoundSerializer(), 'Round')
        self.serialization.register_serializer(
            PlayerInTournamentSerializer(), 'PlayerInTournament')
        self.serialization.register_serializer(
            DateTimeSerializer(), 'TinyDate')
        # self.serialization.register_serializer(TournamentSerializer(), 'Tournament')
        # self.serialization.register_serializer(PlayerSerializer(), 'Player')
        self.db = TinyDB(self.DATA_FOLDER / f'{self.name}.json',
                         create_dirs=True, storage=self.serialization,
                         indent=4)

    def all(self):
        li = []
        for dictionary in self.db.all():
            li.append(self.CLASSES[self.name].from_dict(dictionary))
        return li

    def get(self, **kwargs):
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
        dictionary = self.db.get(doc_id=uuid)
        return self.CLASSES[self.name].from_dict(dictionary)

    def update(self, obj):
        self.db.update(obj.cleaned_data, doc_ids=[obj.uuid])

    def remove(self, obj):
        self.db.remove(doc_ids=[obj.uuid])
