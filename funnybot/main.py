from discord import Client
import logging
import random
import json
import os

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)


class FunnyBot(Client):
    jokes = json.load(open('data/jokes.json'))
    austin_powers_quotes = json.load(open('data/austin_powers_quotes.json'))
    star_wars_quotes = json.load(open('data/star_wars_quotes.json'))

    async def on_ready(self):
        logger.info(f'{self.user} is online!')

    async def on_message(self, message):
        if self.user == message.author:
            return

        response = None

        if message.content == '/help':
            response = '\n'.join((
                'Here are the commands you can use to interact with me:',
                '**/joke** --- receive a random joke.',
                '**/austinpowers** --- receive a random Austin Powers quote.',
                '**/starwars** --- receive a random quote from Star Wars.'
            ))
        elif message.content == '/joke':
            response = random.choice(self.jokes)
        elif message.content == '/austinpowers':
            response = random.choice(self.austin_powers_quotes)
        elif message.content == '/starwars':
            response = random.choice(self.star_wars_quotes)

        if response:
            logger.info(f'{message.author}: {message.content}')
            await message.channel.send(response)


if __name__ == '__main__':
    client = FunnyBot()
    client.run(os.environ.get('DISCORD_TOKEN'))
