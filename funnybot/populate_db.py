import asyncio
from db import database
from db.models import models, Joke
import json


FILES_DIR = 'data/'


async def populate_austin_powers_quotes_table():
    filename = FILES_DIR + 'austin_powers_quotes.json'

    with open(filename) as file:
        data = json.load(file)

    for text in data:
        await Joke.objects.get_or_create(text=text, type='Austin Powers', defaults={})

async def populate_insults_table():
    filename = FILES_DIR + 'insults.json'

    with open(filename) as file:
        data = json.load(file)

    for text in data:
        await Joke.objects.get_or_create(text=text, type='Insult', defaults={})


async def populate_jokes_table():
    filename = FILES_DIR + 'jokes.json'

    with open(filename) as file:
        data = json.load(file)

    for text in data:
        await Joke.objects.get_or_create(text=text, type='Joke', defaults={})


async def populate_star_wars_quotes_table():
    filename = FILES_DIR + 'star_wars_quotes.json'

    with open(filename) as file:
        data = json.load(file)

    for text in data:
        await Joke.objects.get_or_create(text=text, type='Star Wars', defaults={})


async def main():
    await models.create_all()
    await database.connect()
    tasks = [
        asyncio.create_task(func())
        for func in (
            populate_austin_powers_quotes_table,
            populate_insults_table,
            populate_jokes_table,
            populate_star_wars_quotes_table
        )
    ]
    await asyncio.gather(*tasks)
    await database.disconnect()


if __name__ == '__main__':
    asyncio.run(main())
    print('Done!')
