package config

import (
	"encoding/json"
	"fmt"
)

var CONFIG_BUFFER string = "{\"ip\":\"127.10.100.100+\"}"

type Config_t struct {
	IP string
}

func Config_initialize(config_t *Config_t, ConfigStr string) {
	byt := []byte(ConfigStr)[:len(ConfigStr)]
	var dat map[string]interface{}
	if err := json.Unmarshal(byt, &dat); err != nil {
		panic(err)
	}

	config_t.IP = fmt.Sprint(dat["ip"])
}
