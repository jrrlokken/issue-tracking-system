import os
import functools

from flask import Flask, request, render_template, redirect, flash, jsonify
from flask import session, make_response, g
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin
from flask_login import login_user, logout_user, current_user, login_required
from flask_debugtoolbar import DebugToolbarExtension
# from models import db, connect_db, User, Issue

app = Flask(__name__)

app.config['SECRET_KEY'] = "thisisasecret88"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///issue_tracker'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

debug = DebugToolbarExtension(app)
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users.login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/")
def show_index():
    return render_template('index.html')