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
    summary = db.Column(db.Text)
    text = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, nullable=False, default=1)
    reporter = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    assignee = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    priority = db.Column(db.Integer, nullable=False, default=1)
    status_code = db.Column(db.Integer, nullable=False, default=1)
    resolution = db.Column(db.Integer, nullable=False, default=1)
    resolution_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)


class Role(db.Model):
    """Role model."""

    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    role_name = db.Column(db.String)
