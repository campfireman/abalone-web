import uuid
from datetime import datetime

import mongoengine as mge
from abalone_engine.enums import Direction

from . import enums, settings


class UuidField(mge.StringField):
    def __init__(self, *args, **kwargs):
        kwargs['default'] = UuidField.generate_uuid
        super().__init__(*args, **kwargs)

    @classmethod
    def generate_uuid(cls) -> str:
        return str(uuid.uuid4())


class User(mge.Document):
    username = mge.StringField(
        min_length=settings.USERNAME_MIN_LENGTH,
        max_length=settings.USERNAME_MAX_LENGTH,
    )
    password = mge.StringField()
    email = mge.EmailField()
    created_at = mge.DateTimeField(default=datetime.utcnow)

    def __str__(self):
        return self.username


class Move(mge.EmbeddedDocument):
    ply = mge.IntField()
    first = mge.StringField(
        max_length=2,
    )
    last = mge.StringField(
        max_length=2,
    )
    direction = mge.EnumField(Direction)


class Game(mge.Document):
    black = mge.ReferenceField('User', reverse_delete_rule=mge.NULLIFY)
    white = mge.ReferenceField('User', reverse_delete_rule=mge.NULLIFY)
    state = mge.EnumField(enums.GameState, default=enums.GameState.CREATED)
    starting_formation = mge.EnumField(enums.Formation)
    moves = mge.EmbeddedDocumentListField('Move')
    created_at = mge.DateTimeField(default=datetime.utcnow)
