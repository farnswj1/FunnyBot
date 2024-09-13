use std::collections::HashMap;
use std::{env, fs};

use dotenv::dotenv;
use serenity::async_trait;
use serenity::model::channel::Message;
use serenity::model::gateway::Ready;
use serenity::prelude::{Client, Context, EventHandler, GatewayIntents};
use sqlx::postgres::PgPoolOptions;
use sqlx::prelude::FromRow;
use sqlx::{query_as, PgPool};
use tracing::{error, info};

struct Handler {
    database: PgPool,
    map: HashMap<String, String>,
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

        info!("{:}: {:}", msg.author.name, msg.content);

        let response = {
            if let Some(category) = self.map.get(&msg.content) {
                let joke =
                    query_as::<_, Joke>("SELECT text FROM jokes WHERE type = $1 ORDER BY RANDOM() LIMIT 1")
                    .bind(category)
                    .fetch_one(&self.database)
                    .await
                    .unwrap();

                joke.text
            } else {
                self.help_text.to_string()
            }
        };

        let dm = msg.channel_id.say(&context.http, response).await;

        if let Err(error) = dm {
            error!("Error when direct messaging user: {error:?}");
        }
    }

    async fn ready(&self, _: Context, ready: Ready) {
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
    let map = HashMap::from([
        ("/austinpowers".to_string(), "Austin Powers".to_string()),
        ("/insult".to_string(), "Insult".to_string()),
        ("/joke".to_string(), "Joke".to_string()),
        ("/starwars".to_string(), "Star Wars".to_string()),
    ]);
    let help_text = fs::read_to_string("./data/help.txt").expect("Read the file");
    let handler = Handler { database, map, help_text };

    let mut client = Client::builder(&token, intents)
        .event_handler(handler)
        .await
        .expect("Err creating client");

    if let Err(error) = client.start().await {
        error!("Client error: {error:?}");
    }
}
