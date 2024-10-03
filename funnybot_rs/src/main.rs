use std::{env, fs};

use dotenvy::dotenv;
use serenity::all::{
    Command,
    CreateCommand,
    CreateInteractionResponse,
    CreateInteractionResponseMessage,
    Interaction
};
use serenity::async_trait;
use serenity::model::channel::Message;
use serenity::model::gateway::Ready;
use serenity::prelude::{Client, Context, EventHandler, GatewayIntents};
use sqlx::postgres::PgPoolOptions;
use sqlx::prelude::FromRow;
use sqlx::{query_as, PgPool};
use tracing::{error, info};

const COMMANDS: &'static [[&'static str; 2]] = &[
    ["joke", "Receive a random joke."],
    ["insult", "Receive a random insult."],
    ["austinpowers", "Receive a random Austin Powers quote."],
    ["starwars", "Receive a random quote from Star Wars."]
];

struct Handler {
    database: PgPool,
    help_text: String,
}

#[derive(FromRow)]
struct Joke {
    text: String
}

#[async_trait]
impl EventHandler for Handler {
    async fn message(&self, context: Context, msg: Message) {
        // Ignore all messages created by the bot itself.
        if msg.author.id == context.cache.current_user().id {
            return;
        }

        info!("{}: {}", msg.author.name, msg.content);
        let dm = msg.channel_id.say(&context.http, &self.help_text).await;

        if let Err(error) = dm {
            error!("Error when direct messaging user: {error:?}");
        }
    }

    async fn interaction_create(&self, context: Context, interaction: Interaction) {
        if let Interaction::Command(command) = interaction {
            info!("{}: {}", command.user.name, command.data.name);

            let category = match command.data.name.as_str() {
                "joke" => "Joke",
                "insult" => "Insult",
                "austinpowers" => "Austin Powers",
                "starwars" => "Star Wars",
                _ => "Joke"
            };

            let joke =
                query_as::<_, Joke>("SELECT text FROM jokes WHERE type = $1 ORDER BY RANDOM() LIMIT 1")
                .bind(category)
                .fetch_one(&self.database)
                .await
                .unwrap();

            let data = CreateInteractionResponseMessage::new().content(joke.text);
            let message = CreateInteractionResponse::Message(data);
            let dm = command.create_response(&context.http, message).await;

            if let Err(error) = dm {
                error!("Cannot respond to slash command: {error}");
            }
        }
    }

    async fn ready(&self, context: Context, ready: Ready) {
        for &[name, description] in COMMANDS.iter() {
            let command = CreateCommand::new(name).description(description);
            let response = Command::create_global_command(&context.http, command).await;

            if let Err(error) = response {
                error!("Unable to register command: {error}");
            }
        }

        info!("{} #{:?} is online!", ready.user.name, ready.user.discriminator.unwrap());
    }
}

#[tokio::main]
async fn main() {
    dotenv().ok();
    tracing_subscriber::fmt::init();

    let token = env::var("DISCORD_TOKEN").expect("Discord token");
    let database_url = env::var("DATABASE_URL").expect("Database URL");

    let database = PgPoolOptions::new()
        .max_connections(5)
        .connect(&database_url)
        .await
        .expect("Connected to database");

    let intents = GatewayIntents::DIRECT_MESSAGES;
    let help_text = fs::read_to_string("./data/help.txt").expect("Read the file");
    let handler = Handler { database, help_text };

    let mut client = Client::builder(&token, intents)
        .event_handler(handler)
        .await
        .expect("Err creating client");

    if let Err(error) = client.start().await {
        error!("Client error: {error:?}");
    }
}
