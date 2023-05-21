from discord import Client, Intents
from db import database
from db.models import Joke
from settings import DISCORD_TOKEN
import random
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

        match content := message.content:
            case '/help':
                response = self.help_text
            case '/austinpowers' | '/insult' | '/joke' | '/starwars':
                type = self.type_map.get(content)
                joke = random.choice(await Joke.objects.filter(type=type).all())
                response = joke.text
            case _:
                response = None

        if response:
            logger.info(f'{author}: {content}')
            await message.channel.send(response)


if __name__ == '__main__':
    client = FunnyBot(intents=Intents.default())
    client.run(DISCORD_TOKEN)
