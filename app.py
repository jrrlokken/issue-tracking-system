import os
import requests

from flask import Flask, request, render_template, redirect, flash, jsonify, url_for
from flask import session
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin
from flask_login import login_user, logout_user, current_user, login_required
from flask_debugtoolbar import DebugToolbarExtension

from dotenv import load_dotenv

from forms import *
from models import db, connect_db, User, Issue, Comment, Priority, Status, Category, Role

load_dotenv()
bcrypt = Bcrypt()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgres:///issue_tracker')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'keepitsecretkeepitsafe!')

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


#############################################################
# Index routes


@app.route("/", methods=['GET', 'POST'])
def index():
    """Index view."""

    if current_user.is_authenticated:

        if current_user.role == 2:
            issues = Issue.query.order_by(Issue.id).all()
        elif current_user.roles.role_label == 'assignee':
            issues = Issue.query.order_by(Issue.id).filter((Issue.assignee == current_user.id) | (Issue.status != 2)).all()
        else:
            issues = Issue.query.order_by(Issue.id).filter(Issue.reporter == current_user.id, Issue.status != 2).all()

        return render_template('base/index.html', issues=issues)

    return render_template('base/index.html')



@app.route("/register", methods=["GET", "POST"])
def register():
    """Provide register form and handle submit."""

    if current_user.is_authenticated:
        return redirect("/")

    form = AddUserForm()

    if form.validate_on_submit():
        if User.query.filter(User.email == form.email.data).first():
            # error, there already is a user using this email address
            flash(f"{form.email.data} has already been registered", "warning")
            return redirect("/register")

        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        password = form.password.data
        user = User.register(email, first_name, last_name, password)

        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("Registered.", "success")

        return redirect("/")

    return render_template('users/register.html', form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Provide login form and handle submit."""

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not bcrypt.check_password_hash(user.password, form.password.data):
            flash('Invalid email or password', 'warning')
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

    return redirect("/")


#############################################################
# User routes

@app.route("/users")
@login_required
def list_users():
    """List users."""

    if current_user.roles.role_label != 'admin':
        flash('You must be an admin, sorry.', 'danger')
        return redirect(url_for('index'))

    users = User.query.all()
    return render_template('users/list.html', users=users)

@app.route("/users/<int:user_id>", methods=["GET"])
@login_required
def user_detail(user_id):
    """User detail"""

    user = User.query.get_or_404(user_id)

    return render_template("users/detail.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=["GET", "POST"])
@login_required
def edit_user(user_id):
    """Edit user form and handler."""

    user = User.query.get_or_404(user_id)
    form = EditUserForm(obj=user)

    roles = Role.query.all()
    roles_list = [(r.role_id, r.role_label) for r in roles]
    
    form.role.choices = roles_list

    if form.validate_on_submit():
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        role = form.role.data

        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.role = role

        db.session.commit()
        flash("User edited", "success")
        return redirect(f"/users/{user.id}")

    return render_template("users/edit.html", user=user, form=form)

@app.route("/users/<int:user_id>/delete", methods=["POST"])
@login_required
def delete_user(user_id):
    """Delete an existing user.  For admins only."""

    if current_user.roles.role_label != 'admin':
        flash('You must be an admin, sorry.', 'danger')
        return redirect("/users")
    
    if request.method == "POST":
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        flash(f"User {user.first_name} {user.last_name} has been deleted.", "success")
        return redirect("/users")


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
    statuses = Status.query.all()
    statuses_list = [(s.status_id, s.status_label) for s in statuses]

    form.category.choices = categories_list
    form.priority.choices = priorities_list
    form.status.choices = statuses_list
    
    if form.validate_on_submit():
        title = form.title.data
        text = form.text.data
        category = form.category.data
        priority = form.priority.data
        status = form.status.data

        issue.title = title
        issue.text = text
        issue.category = category
        issue.priority = priority
        issue.status = status

        # db.session.merge(issue)
        # db.session.flush()
        db.session.commit()
        flash("Issue updated", "success")
        return redirect("/")

    return render_template("issues/edit.html", issue=issue, form=form)


@app.route("/issues/<int:issue_id>/delete", methods=["POST"])
@login_required
def delete_issue(issue_id):
    """Delete an existing issue.  For admins only."""

    if current_user.role != 2:
        flash("Admin privileges required.", "danger")
        return redirect("/")
    
    if request.method == "POST":
        issue = Issue.query.get_or_404(issue_id)
        db.session.delete(issue)
        db.session.commit()
        flash(f"Issue '{issue.title}' has been deleted.", "success")
        return redirect("/")

#############################################################
# Comment routes.

@app.route("/issues/<int:issue_id>/comments/new", methods=["POST"])
@login_required
def new_comment(issue_id):
    """New comment form and handler."""

    form = NewCommentForm()
    issue = Issue.query.get_or_404(issue_id)

    if form.validate_on_submit():
        comment_text = form.text.data
        comment = Comment(comment_text=comment_text, comment_issue=issue_id, comment_user=current_user.id)

        db.session.add(comment)
        db.session.commit()
        flash("Comment added.", "success")
        return redirect(f"/issues/{issue_id}")

    return render_template("comments/new.html", issue=issue, form=form)

    
@app.route("/comments/<int:comment_id>/delete", methods=["POST"])
@login_required
def delete_comment(comment_id):
    """Delete an existing comment.  For admins only."""

    if current_user.roles.role_label != 'admin':
        if request.method == "POST":
            comment = Comment.query.get_or_404(comment_id)
            db.session.delete(comment)
            db.session.commit()
            flash(f"Comment #{comment_id} has been deleted.", "success")
            return redirect("/")
    
    flash("Admin privileges required.", "danger")
    return redirect("/")


#############################################################
# Miscellaneous routes

@app.route('/search')
@login_required
def search():
    """Search for issues."""
    search = request.args.get('search')
    issues = Issue.query.order_by((Issue.created_at.desc())).filter((Issue.title.ilike("%" + search + "%") | Issue.text.ilike("%" + search + "%"))).all()
        
    return render_template("base/index.html", issues=issues)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('base/404.html'), 404




