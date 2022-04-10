from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from config import BaseConfig
import time

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


def add_agent(os, host_name, ip, ram):
    if not db.session.query(db.exists().where(Agent.ip == ip)).scalar():
        agent = Agent(os, host_name, ip, ram)
        db.session.add(agent)
        db.session.flush()
        agent_id = agent.id
        print(agent_id)
        db.session.add(CommandQueue(agent_id, 'ls', 'asd'))
        db.session.commit()
        print(agent_id)
        return agent.id


@app.route('/', methods=['GET', 'POST'])
@login_required
def home():  # put application's code here
    output = ""
    if request.method == "POST":
        command = request.form['command']
        agent_id = request.form['id']
        res = CommandQueue.query.filter_by(id=agent_id).first()
        res.command = command
        db.session.commit()
        time.sleep(1)
        res = CommandQueue.query.filter_by(id=agent_id).first()
        output = res.output

    agents = db.session.query(Agent).all()
    return render_template('index.html', agents=agents, command_out=output)


@app.route('/api/1.1/add_agent', methods=['GET', 'POST'])
def agent_add():
    print(request.method)
    if request.method == 'POST':
        agent_dict = request.json
        id = add_agent(agent_dict['os'], agent_dict['host_name'], agent_dict['ip'], agent_dict['ram'])
        return str(id)


@app.route('/api/1.1/get_command', methods=['GET', 'POST'])
def get_command():
    print(request.method)
    if request.method == 'POST':
        agent_id = request.json['id']
        res = CommandQueue.query.filter_by(id=agent_id).first()
        return res.command


@app.route('/api/1.1/command_out', methods=['GET', 'POST'])
def command_out():
    print(request.method)
    if request.method == 'POST':
        output = request.json['output']
        agent_id = request.json['id']
        # print(output, agent_id)
        agent = CommandQueue.query.filter_by(id=agent_id).first()
        agent.output = output
        agent.command = 'None'
        # print(agent.output)
        db.session.commit()
        return 'Received'


@app.route('/welcome')
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


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were just logged out!')
    return redirect(url_for('welcome'))


if __name__ == '__main__':
    app.run()
