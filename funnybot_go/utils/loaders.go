package utils

import (
	"io"
	"os"
)

func LoadFile(filename string) string {
	jsonFile, err := os.Open(filename)

	if err != nil {
		Logger.Panic(err)
	}

	defer jsonFile.Close()
	byteValue, _ := io.ReadAll(jsonFile)
	return string(byteValue)
}
