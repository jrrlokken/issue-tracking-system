# import os
# import functools

from flask import Flask, request, render_template, redirect, flash, jsonify
from flask import session, make_response, g
# from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin
from flask_login import login_user, logout_user, current_user, login_required
from flask_debugtoolbar import DebugToolbarExtension
from forms import *
from models import db, connect_db, User, Issue, Role

app = Flask(__name__)

app.config.from_envvar('ITS_APP_SETTINGS')

debug = DebugToolbarExtension(app)
connect_db(app)
db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/")
def show_index():
    """Index view."""

    return render_template('base/index.html')


@app.route("/register", methods=["GET", "POST"])
def show_register_form():
    form = AddUserForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        return redirect("/")

    return render_template('users/register.html', form=form)


@app.route("/login", methods=["GET", "POST"])
def login_form():
    """Provide login form and handle submission."""

    form = LoginForm()

    return render_template('users/login.html', form=form)


@app.route("/logout")
def logout():
    """Logout route."""

    if current_user:
        logout_user()
        flash("Logged out")

    return redirect("/login")
