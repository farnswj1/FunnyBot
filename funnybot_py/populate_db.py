import asyncio
from db import database
from db.models import models, Joke
import json


async def populate_db_partition(filename: str, _type: str):
    """Load the file and add its values to the database"""
    with open(filename) as file:
        data = json.load(file)

    for text in data:
        await Joke.objects.get_or_create(text=text, type=_type, defaults={})


async def main():
    """Populate the database"""
    await models.create_all()
    await database.connect()

    filenames = {
        'Austin Powers': 'austin_powers_quotes.json',
        'Insult': 'insults.json',
        'Joke': 'jokes.json',
        'Star Wars': 'star_wars_quotes.json'
    }
    tasks = [
        asyncio.create_task(populate_db_partition(f'data/{filename}', _type))
        for _type, filename in filenames.items()
    ]
    await asyncio.gather(*tasks)

    await database.disconnect()


if __name__ == '__main__':
    asyncio.run(main())
    print('Done!')
