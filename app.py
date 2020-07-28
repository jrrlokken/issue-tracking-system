# import os
# import functools

from flask import Flask, request, render_template, redirect, flash, jsonify, url_for
from flask import session, make_response

from flask_login import LoginManager, UserMixin
from flask_login import login_user, logout_user, current_user, login_required
from flask_debugtoolbar import DebugToolbarExtension

from dotenv import load_dotenv
import os

from forms import *
from models import db, connect_db, User, Issue, Comment, Role, Priority, Resolution, Status, Category
# from helpers import friendly_date


load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('SQLALCHEMY_DATABASE_URI'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

debug = DebugToolbarExtension(app)
connect_db(app)

db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    """Login manager load user method."""

    return User.query.get(int(user_id))


@app.route("/")
def index():
    """Index view."""

    issues = Issue.query.all()
    return render_template('base/index.html', issues=issues)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Provide register form and handle submit."""

    if current_user.is_authenticated:
        return redirect("/")

    form = AddUserForm()

    if form.validate_on_submit():
        if User.query.filter(User.email == form.email.data).first():
            # error, there already is a user using this bank address
            flash(f"{form.email.data} has already been registered", "danger")
            return redirect("/register")

        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        password = form.password.data
        user = User.register(email, first_name, last_name, password)

        db.session.add(user)
        db.session.commit()
        flash("Registered.", "success")

        return redirect("/login")

    return render_template('users/register.html', form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Provide login form and handle submit."""

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(email=form.email.data, password=form.password.data)
        if user is None:
            flash('Invalid email or password', 'danger')
            return redirect(url_for('login'))
        login_user(user)
        flash("Welcome!", "success")
        return redirect(url_for('index'))
    return render_template('users/login.html', form=form)


@app.route("/logout")
def logout():
    """Logout route."""

    if current_user:
        logout_user()
        flash("Logged out", "success")

    return redirect("/login")


#############################################################
# Issue routes

@app.route("/issues/new", methods=["GET", "POST"])
@login_required
def new_issue():
    """New issue form and handler."""

    categories = Category.query.all()
    categories_list = [(c.category_id, c.category_label) for c in categories]
    priorities = Priority.query.all()
    priorities_list = [(p.priority_id, p.priority_label) for p in priorities]

    # import pdb; pdb.set_trace()

    form = NewIssueForm(category=0, priority=1)
    form.category.choices = categories_list
    form.priority.choices = priorities_list

    if form.validate_on_submit():
        title = form.title.data
        text = form.text.data
        category = form.category.data
        priority = form.priority.data

        issue = Issue(title=title, text=text, category=category, priority=priority, reporter=current_user.id)
        db.session.add(issue)
        db.session.commit()
        flash("Issue submitted", "success")
        return redirect("/")

    return render_template('issues/new.html', form=form)


@app.route("/issues/<int:issue_id>", methods=["GET"])
@login_required
def issue_detail(issue_id):
    """Issue detail"""

    issue = Issue.query.get_or_404(issue_id)
    form = NewCommentForm()

    return render_template("issues/detail.html", issue=issue, form=form)


@app.route("/issues/<int:issue_id>/edit", methods=["GET", "POST"])
@login_required
def edit_issue(issue_id):
    """Edit issue form and handler."""

    issue = Issue.query.get_or_404(issue_id)
    form = EditIssueForm(obj=issue)

    categories = Category.query.all()
    categories_list = [(c.category_id, c.category_label) for c in categories]
    priorities = Priority.query.all()
    priorities_list = [(p.priority_id, p.priority_label) for p in priorities]
    form.category.choices = categories_list
    form.priority.choices = priorities_list
    
    if form.validate_on_submit():
        title = form.title.data
        text = form.text.data
        category = form.category.data
        priority = form.priority.data

        issue.title = title
        issue.text = text
        issue.category = category
        issue.priority = priority

        db.session.commit()
        flash("Issue edited", "success")
        return redirect(f"/issues/{{ issue.id }}")

    return render_template("issues/edit.html", issue=issue, form=form)



#############################################################
# Comment routes.

@app.route("/issues/<int:issue_id>/comments/new", methods=["GET", "POST"])
@login_required
def new_comment(issue_id):
    """New comment form and handler."""

    form = NewCommentForm()

    return render_template("comments/new.html", issue_id=issue_id, form=form)

    












# with app.test_request_context():
#     print(url_for('index'))
#     print(url_for('register'))
#     print(url_for('login'))
#     print(url_for('login', next='/'))
#     print(url_for('logout'))
