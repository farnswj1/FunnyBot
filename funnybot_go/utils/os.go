package utils

import (
	"os"
	"strings"

	"github.com/joho/godotenv"
)

type EnvMap map[string]string
var Env = loadEnv()

func loadEnv() EnvMap {
	godotenv.Load()
	items := EnvMap{}

	for _, item := range os.Environ() {
		key, val, _ := strings.Cut(item, "=")
		items[key] = val
	}

	return items
}

func (env EnvMap) Get(key, fallback string) string {
	if value, exists := env[key]; exists {
		return value
	}

	return fallback
}
