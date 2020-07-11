from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, BooleanField, SelectField
from wtforms.validators import InputRequired, Optional, URL, NumberRange, AnyOf

# Form classes


class AddUserForm(FlaskForm):
    """Form for user registration."""

    email = StringField("Email", validators=[InputRequired()])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])
    password = StringField("Password", validators=[InputRequired()])


class LoginForm(FlaskForm):
    """Login form."""

    email = StringField("Email", validators=[InputRequired()])
    password = StringField("Password", validators=[InputRequired()])


class EditUserForm(FlaskForm):
    """Form to edit user details."""

    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])
    password = StringField("Password", validators=[InputRequired()])


class AddIssueForm(FlaskForm):
    """Form to enter new issue."""
    title = StringField("Title", validators=[InputRequired()])
    summary = StringField("Issue Summary", validators=[InputRequired()])
    text = TextAreaField("Issue Description", validators=[InputRequired()])


class EditIssueForm(FlaskForm):
    """Form to edit existing issue."""
    title = StringField("Title", validators=[InputRequired()])
    summary = StringField("Issue Summary", validators=[InputRequired()])
    text = TextAreaField("Issue Description", validators=[InputRequired()])
    priority = SelectField()
