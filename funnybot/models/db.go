package models

import (
  "funnybot/utils"

  "gorm.io/driver/postgres"
  "gorm.io/gorm"
)

var DB = connectDatabase()

func connectDatabase() *gorm.DB {
  utils.Logger.Println("Connecting to database...")

  config := &gorm.Config{}

  database, err := gorm.Open(
    postgres.Open(utils.Env["DATABASE_URL"]),
    config,
  )

  if err != nil {
    utils.Logger.Panic(err.Error())
  }

  if err = database.AutoMigrate(&Joke{}); err != nil {
    utils.Logger.Panic(err.Error())
  }

  utils.Logger.Println("Connected to database!")
  return database
}
