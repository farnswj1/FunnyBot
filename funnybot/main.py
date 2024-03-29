from discord import Client, Intents
from sqlalchemy.sql.expression import func
from db import database
from db.models import Joke
from settings import DISCORD_TOKEN
import logging


logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)


class FunnyBot(Client):
    type_map = {
        '/austinpowers': 'Austin Powers',
        '/insult': 'Insult',
        '/joke': 'Joke',
        '/starwars': 'Star Wars'
    }

    async def setup_hook(self):
        await database.connect()

        with open('data/help.txt') as file:
            self.help_text = file.read()

    async def close(self):
        await super().close()
        await database.disconnect()

    async def on_ready(self):
        logger.info(f'{self.user} is online!')

    async def on_message(self, message):
        author = message.author

        if self.user == author:
            return

        content = message.content

        if content in self.type_map:
            _type = self.type_map.get(content)
            joke = await Joke.objects.filter(type=_type).order_by(func.random()).first()
            response = joke.text
        elif content == '/help':
            response = self.help_text
        else:
            response = None

        if response:
            logger.info(f'{author}: {content}')
            await message.channel.send(response)


if __name__ == '__main__':
    client = FunnyBot(intents=Intents.default())
    client.run(DISCORD_TOKEN)
