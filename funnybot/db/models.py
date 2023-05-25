from orm import ModelRegistry, Model, UUID, String
from orm.models import QuerySet
from sqlalchemy.sql.expression import Function
from db import database
import uuid


# monkey patch method to accept SQLAlchemy function classes
original_prepare_order_by = QuerySet._prepare_order_by


def _prepare_order_by(self, order_by):
    return order_by if isinstance(order_by, Function) else original_prepare_order_by(order_by)


QuerySet._prepare_order_by = _prepare_order_by


models = ModelRegistry(database=database)


class Joke(Model):
    tablename = 'jokes'
    registry = models
    fields = {
        'id': UUID(primary_key=True, default=uuid.uuid4),
        'text': String(max_length=1024, unique=True),
        'type': String(max_length=20)
    }
