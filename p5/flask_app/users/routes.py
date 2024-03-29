from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required, login_user, logout_user

from .. import bcrypt
from ..forms import RegistrationForm, LoginForm, UpdateUsernameForm
from ..models import User



# Create a BluePrint object for this app
# Package name is a folder name that has __init__
users_bp = Blueprint('users_bp', __name__)

# Use the blueeprint in the decorator
@users_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("movies_bp.index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed)
        user.save()

        return redirect(url_for("users_bp.login"))

    return render_template("register.html", title="Register", form=form)


@users_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("movies_bp.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()

        if user is not None and bcrypt.check_password_hash(
            user.password, form.password.data
        ):
            login_user(user)
            return redirect(url_for("users_bp.account"))
        else:
            flash("Login failed. Check your username and/or password")
            return redirect(url_for("users_bp.login"))

    return render_template("login.html", title="Login", form=form)


@users_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("movies_bp.index"))


@users_bp.route("/account", methods=["GET", "POST"])
@login_required
def account():
    username_form = UpdateUsernameForm()

    if username_form.validate_on_submit():
        # current_user.username = username_form.username.data
        current_user.modify(username=username_form.username.data)
        current_user.save()
        return redirect(url_for("users_bp.account"))

    return render_template(
        "account.html",
        title="Account",
        username_form=username_form,
    )




