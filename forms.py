from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, BooleanField, SelectField, PasswordField
from wtforms.validators import InputRequired, Optional, NumberRange, AnyOf, Length, EqualTo, URL

# Form classes


class AddUserForm(FlaskForm):
    """Form for user registration."""

    email = StringField("Email", validators=[InputRequired()])
    first_name = StringField("First Name", validators=[
                             InputRequired(), Length(min=2, max=20)])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(min=2, max=20)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=32), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField("Confirm Password")
    accept_tos = BooleanField("I accept the Terms of Service", validators=[InputRequired()])


class LoginForm(FlaskForm):
    """Login form."""

    email=StringField("Email", validators=[InputRequired()])
    password=PasswordField("Password", validators=[InputRequired()])


class EditUserForm(FlaskForm):
    """Form to edit user details."""

    first_name=StringField("First Name", validators=[InputRequired()])
    last_name=StringField("Last Name", validators=[InputRequired()])
    password=PasswordField("Password", validators=[InputRequired()])


class AddIssueForm(FlaskForm):
    """Form to enter new issue."""
    title=StringField("Title", validators=[InputRequired()])
    summary=StringField("Issue Summary", validators=[InputRequired()])
    text=TextAreaField("Issue Description", validators=[InputRequired()])
    priority=SelectField()


class EditIssueForm(FlaskForm):
    """Form to edit existing issue."""
    title=StringField("Title", validators=[InputRequired()])
    summary=StringField("Issue Summary", validators=[InputRequired()])
    text=TextAreaField("Issue Description", validators=[InputRequired()])
    priority=SelectField()
