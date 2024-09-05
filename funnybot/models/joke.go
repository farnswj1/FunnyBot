package models

import "github.com/google/uuid"

type Joke struct {
	Id   uuid.UUID `gorm:"column:id;type:uuid;default:gen_random_uuid();primary_key"`
	Text string    `gorm:"column:text;type:varchar(1024);unique;not null"`
	Type string    `gorm:"column:type;type:varchar(20);not null"`
}
