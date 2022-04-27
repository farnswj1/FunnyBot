# Funny Bot
This is a Discord bot that tries to make you laugh.


## Requirements
This project uses Docker and Docker Compose. Please install them before continuing.
Also, you must have a Discord bot set up in order to use this program.


## Setup
First, create a ```.env``` file inside the ```app``` directory.
Then, add the token from your Discord bot to ```DISCORD_TOKEN```, as shown below:
```
DISCORD_TOKEN=[token goes here]
```

Then, run ```docker-compose up -d --build``` to build the image and run the container.


## How to Use
Once the container is running, send a message to the Discord bot. Commands are provided
to get a particular type of joke.

For a random joke, enter ```/joke```.

For an Austin Powers quote, enter ```/austinpowers```.
