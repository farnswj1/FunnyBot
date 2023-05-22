from orm import ModelRegistry, Model, UUID, String
from db import database
import uuid


models = ModelRegistry(database=database)


class Joke(Model):
    tablename = 'jokes'
    registry = models
    fields = {
        'id': UUID(primary_key=True, default=uuid.uuid4),
        'text': String(max_length=1024, unique=True),
        'type': String(max_length=20)
    }
