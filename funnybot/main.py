from discord import Client, Intents
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
        author = message.author

        if self.user == author:
            return

        match content := message.content:
            case '/help':
                response = '\n'.join((
                    'Here are the commands you can use to interact with me:',
                    '**/joke** --- receive a random joke.',
                    '**/austinpowers** --- receive a random Austin Powers quote.',
                    '**/starwars** --- receive a random quote from Star Wars.'
                ))
            case '/joke':
                response = random.choice(self.jokes)
            case '/austinpowers':
                response = random.choice(self.austin_powers_quotes)
            case '/starwars':
                response = random.choice(self.star_wars_quotes)
            case _:
                response = None

        if response:
            logger.info(f'{author}: {content}')
            await message.channel.send(response)


if __name__ == '__main__':
    client = FunnyBot(intents=Intents.default())
    client.run(os.getenv('DISCORD_TOKEN'))
