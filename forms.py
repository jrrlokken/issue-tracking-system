from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, BooleanField, SelectField, PasswordField, HiddenField
from wtforms.validators import InputRequired, DataRequired, Optional, NumberRange, AnyOf, Length, EqualTo, URL

# Form classes


class AddUserForm(FlaskForm):
    """Form for user registration."""

    email = StringField("Email", validators=[InputRequired()])
    first_name = StringField("First Name", validators=[
                             InputRequired(), Length(min=2, max=20)])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(min=2, max=20)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=32), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField("Confirm Password", validators=[InputRequired()])
    # accept_tos = BooleanField("I accept the Terms of Service", validators=[InputRequired()])


class LoginForm(FlaskForm):
    """Login form."""

    email = StringField("Email", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])


class EditUserForm(FlaskForm):
    """Form to edit user details."""

    first_name=StringField("First Name", validators=[InputRequired()])
    last_name=StringField("Last Name", validators=[InputRequired()])
    password=PasswordField("Password", validators=[InputRequired()])


class NewIssueForm(FlaskForm):
    """Form to enter new issue."""

    title = StringField("Title", validators=[InputRequired()])
    text = TextAreaField("Issue Description", validators=[InputRequired()])
    category = SelectField("Category",
                            validators=[InputRequired()],
                            coerce=int)
    priority = SelectField("Priority",
                            validators=[InputRequired()],
                            coerce=int)



class EditIssueForm(FlaskForm):
    """Form to enter new issue."""

    title = StringField("Title", validators=[InputRequired()])
    text = TextAreaField("Issue Description", validators=[InputRequired()])
    category = SelectField("Category",
                            validators=[InputRequired()],
                            coerce=int)
    priority = SelectField("Priority",
                            validators=[InputRequired()],
                            coerce=int)


class NewCommentForm(FlaskForm):
    """Form form new comment."""

    text = TextAreaField("Comment:", validators=[InputRequired()])