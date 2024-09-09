package main

import (
	"funnybot/handlers"
	"funnybot/utils"
	"os"
	"os/signal"
	"syscall"

	"github.com/bwmarrin/discordgo"
)

func getClient(token string) *discordgo.Session {
	client, err := discordgo.New("Bot " + token)

	if err != nil {
		utils.Logger.Panic(err.Error())
	}

	client.Identify.Intents = discordgo.IntentDirectMessages
	client.AddHandler(handlers.OnReady)
	client.AddHandler(handlers.OnMessage)
	return client
}

func main() {
	token := utils.Env["DISCORD_TOKEN"]
	bot := getClient(token)

	if err := bot.Open(); err != nil {
		utils.Logger.Panic(err.Error())
	}

	// Wait here until CTRL-C or other term signal is received.
	stop := make(chan os.Signal, 1)
	signal.Notify(stop, syscall.SIGINT, syscall.SIGTERM, os.Interrupt)
	<-stop

	utils.Logger.Println("Shutting down...")
	bot.Close()
}
