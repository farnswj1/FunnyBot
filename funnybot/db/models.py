from sqlalchemy import Table, Column, Integer, String
from db import metadata


austin_powers_quotes = Table(
    'austin_powers_quotes',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('text', String(256), nullable=False, unique=True)
)

insults = Table(
    'insults',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('text', String(256), nullable=False, unique=True)
)

jokes = Table(
    'jokes',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('text', String(1024), nullable=False, unique=True)
)

star_wars_quotes = Table(
    'star_wars_quotes',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('text', String(256), nullable=False, unique=True)
)
