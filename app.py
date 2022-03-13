import os

from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from dotenv import load_dotenv


load_dotenv()

# create the application object

app = Flask(__name__)

app.database = "agents.db"

app.config.from_object(os.getenv('APP_SETTINGS'))


# create the sqlalchemy object
db = SQLAlchemy(app)


from models import *


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
    db.session.add(Agent(os, host_name, ip, ram))
    db.session.commit()


@app.route('/')
@login_required
def home():  # put application's code here
    agents = db.session.query(Agent).all()
    return render_template('index.html', agents=agents)


@app.route('/api/1.1/add_agent', methods=['GET', 'POST'])
def agent_add():
    print(request.method)
    if request.method == 'POST':
        agent_dict = request.json
        add_agent(agent_dict['os'], agent_dict['host_name'], agent_dict['ip'], agent_dict['ram'])
    return redirect(url_for('home'))


@app.route('/api/1.1/get_command', methods=['GET', 'POST'])
def get_command():
    print(request.method)
    if request.method == 'POST':
        return 'ls'


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
