from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


def connect_db(app):
    db.app = app
    db.init_app(app)


# Models

class User(db.Model):
    """Issue Tracker user."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    password = db.Column(db.Text, nullable=False)
    role = db.Column(db.Text, nullable=False, default='user')

    @classmethod
    def register(cls, email, password):
        """Register a user, hashing their password."""

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        return cls(email=email, password=hashed_utf8)

    @classmethod
    def authenticate(cls, email, password):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        user = User.query.filter_by(email=email).one()
        if user is not None:
            if bcrypt.check_password_hash(user.password, password):
                return user

        return False

    def __repr__(self):
        return '<{}-"{} {}"-{}>'.format(self.id, self.first_name, self.last_name, self.role)


class Issue(db.Model):
    """Issue model."""

    __tablename__ = "issues"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text, nullable=False)
    text = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, nullable=False, default=1)
    reporter = db.Column(db.Integer, db.ForeignKey(
        'users.id'), nullable=False, default=2)
    assignee = db.Column(db.Integer, db.ForeignKey(
        'users.id'), nullable=False, default=3)
    priority = db.Column(db.Integer, nullable=False, default=1)
    status_code = db.Column(db.Integer, nullable=False, default=1)
    resolution = db.Column(db.Integer, nullable=False, default=1)
    # resolution_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())


class Comment(db.Model):
    """Comment model."""

    __tablename__ = "comments"

    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment_date = db.Column(
        db.DateTime, nullable=False, server_default=func.now())
    comment_text = db.Column(db.Text, nullable=False)
    comment_user = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=False)
    comment_issue = db.Column(
        db.Integer, db.ForeignKey('issues.id'), nullable=False)


class Role(db.Model):
    """Role model."""

    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    role_name = db.Column(db.String)


class Priority(db.Model):
    """Priorities model."""

    __tablename__ = "priorities"

    priority_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    priority_label = db.Column(db.String, nullable=False)


class Resolution(db.Model):
    """Priorities model."""

    __tablename__ = "resolutions"

    resolution_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    resolution_label = db.Column(db.String, nullable=False)


class Status(db.Model):
    """Priorities model."""

    __tablename__ = "statuses"

    status_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status_label = db.Column(db.String, nullable=False)
