from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import (
    InputRequired,
    DataRequired,
    NumberRange,
    Length,
    Email,
    EqualTo,
    ValidationError,
)
from flask_bcrypt import Bcrypt
from . import bcrypt

from .models import User


class SearchForm(FlaskForm):
    search_query = StringField(
        "Query", validators=[InputRequired(), Length(min=1, max=100)]
    )
    submit = SubmitField("Search")


class MovieReviewForm(FlaskForm):
    text = TextAreaField(
        "Comment", validators=[InputRequired(), Length(min=5, max=500)]
    )
    submit = SubmitField("Enter Comment")


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=1, max=40)]
    )
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[InputRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is taken")

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError("Email is taken")


class LoginForm(FlaskForm):
    username = StringField(
        "Enter Username", validators=[InputRequired(), Length(min=1, max=40)]
    )

    password = PasswordField("Enter Password", validators=[InputRequired(), Length(min=1)])

    submit = SubmitField("Log In")


class UpdateUsernameForm(FlaskForm):
    username = StringField(
        "Change Username", validators=[InputRequired(), Length(min=1, max=40)]
    )
    # flash message
    submit = SubmitField("Update")


class UpdateProfilePicForm(FlaskForm):
    picture = FileField(
        "Change Avatar",
        validators=[
            FileRequired(), 
            FileAllowed(["jpg", "png"], "Images Only!")
        ]
    )
    submit = SubmitField("Update")


class UpdatePasswordForm(FlaskForm):
    current = PasswordField("Change Password",validators=[InputRequired(), Length(min=1)])
    new_password = PasswordField(validators=[InputRequired(), Length(min=1)])
    confirm = PasswordField(validators=[InputRequired(), EqualTo("new_password")])
    submit = SubmitField("Update")

    # To validate, it has to be named validate_{UpdatePasswordForm.field}
    def validate_current(self, current):
        user = User.objects(username=current_user.username).first()
        if not bcrypt.check_password_hash(user.password, current.data):
            raise ValidationError("Password does not match.")


# Form to save user theme
class DarkModeForm(FlaskForm):
    # hidden submit button
    submit = SubmitField('Submit', render_kw={'hidden': True})