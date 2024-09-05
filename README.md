# Funny Bot
This is a Discord bot that tries to make you laugh.

## Requirements
This project uses Docker and Docker Compose. Please install them before continuing.
Also, you must have a Discord bot set up in order to use this program.

## Setup
### Funny Bot
First, create a ```.env``` file inside the ```funnybot``` directory.
Then, add the token from your Discord bot to ```DISCORD_TOKEN``` and
the ```DATABASE_URL``` configurations, as shown below:
```
DISCORD_TOKEN=[token goes here]
DATABASE_URL=postgresql://postgres:password@postgres:5432/funnybot
```

### PostgreSQL
Create a ```.env``` file inside the ```postgres``` directory with the
following configurations:
```
POSTGRES_DB=funnybot
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
```

Then, run ```docker-compose up -d --build``` to build the image(s) and run the container(s).

### Loading the Data
To populate the database, ```docker exec -it funnybot python populate_db.py```.

## How to Use
Once the container is running and the database is set up, send a message to the Discord bot. Commands are provided
to get a particular type of joke.

For a random joke, enter ```/joke```.

For an Austin Powers quote, enter ```/austinpowers```.

For more, enter ```/help```.
