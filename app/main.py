from discord import Client
import logging
import random
import json
import os

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)


class FunnyBot(Client):
    austin_powers_quotes = json.load(open('data/austin_powers_quotes.json'))
    jokes = json.load(open('data/jokes.json'))

    async def on_ready(self):
        logger.info(f'{self.user} is online!')

    async def on_message(self, message):
        if self.user == message.author:
            return
        elif message.content == '/joke':
            logger.info(f'{message.author}: {message.content}')
            joke = ''.join(random.choice(self.jokes).split('\n'))
            await message.channel.send(joke)
        elif message.content == '/austinpowers':
            logger.info(f'{message.author}: {message.content}')
            quote = random.choice(self.austin_powers_quotes)
            await message.channel.send(quote)


if __name__ == '__main__':
    client = FunnyBot()
    client.run(os.environ.get('DISCORD_TOKEN'))
