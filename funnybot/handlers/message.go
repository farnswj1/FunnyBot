package handlers

import (
	"funnybot/models"
	"funnybot/utils"

	"github.com/bwmarrin/discordgo"
)

var helpText = utils.LoadFile("data/help.txt")
var jokeMap = map[string]string{
	"/austinpowers": "Austin Powers",
	"/insult": "Insult",
	"/joke": "Joke",
	"/starwars": "Star Wars",
}

func OnMessage(s *discordgo.Session, m *discordgo.MessageCreate) {
	// Ignore all messages created by the bot itself.
	if m.Author.ID == s.State.User.ID {
		return
	}

	content := m.Content
	utils.Logger.Printf("%s: %s\n", m.Author, content)

	if jokeType, ok := jokeMap[content]; ok {
		var joke models.Joke

		models.
			DB.
			Model(&models.Joke{}).
			Select("text").
			Where("type = ?", jokeType).
			Order("RANDOM()").
			Take(&joke)

		s.ChannelMessageSend(m.ChannelID, joke.Text)
		return
	}

	s.ChannelMessageSend(m.ChannelID, helpText)
}
