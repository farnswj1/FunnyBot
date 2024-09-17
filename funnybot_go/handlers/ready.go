package handlers

import (
	"funnybot/utils"

	"github.com/bwmarrin/discordgo"
)

func OnReady(s *discordgo.Session, m *discordgo.Ready) {
	utils.Logger.Printf("%s is online!\n", s.State.User)
}
