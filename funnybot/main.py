from discord import Client, Intents
from db import database
from db.models import (
    austin_powers_quotes,
    insults,
    jokes,
    star_wars_quotes
)
from db.operations import get_select_random_record_query
from settings import DISCORD_TOKEN
import logging


logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)


class FunnyBot(Client):
    async def setup_hook(self):
        await database.connect()

        with open('data/help.txt') as file:
            self.help_text = file.read()

    async def on_ready(self):
        logger.info(f'{self.user} is online!')

    async def on_message(self, message):
        author = message.author

        if self.user == author:
            return

        match content := message.content:
            case '/help':
                query = None
                response = self.help_text
            case '/austinpowers':
                query = get_select_random_record_query(austin_powers_quotes)
            case '/insult':
                query = get_select_random_record_query(insults)
            case '/joke':
                query = get_select_random_record_query(jokes)
            case '/starwars':
                query = get_select_random_record_query(star_wars_quotes) 
            case _:
                query = None
                response = None

        if query is not None:
            result = await database.fetch_one(query)
            response = result.text

        if response:
            logger.info(f'{author}: {content}')
            await message.channel.send(response)


if __name__ == '__main__':
    client = FunnyBot(intents=Intents.default())
    client.run(DISCORD_TOKEN)
