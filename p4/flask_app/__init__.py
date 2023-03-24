# 3rd-party packages
from flask import Flask, render_template, request, redirect, url_for
from flask_mongoengine import MongoEngine
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
)
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

# stdlib
import os
from datetime import datetime

# local
from .client import MovieClient

app = Flask(__name__)
# change localhost to 27017
app.config["MONGODB_HOST"] = "mongodb://localhost:27017/project_4"
app.config['SECRET_KEY'] = b'"\x7f\xa1\xc0Q!\x9e:\x1b4\xb7{0\xf0\xd8\xf4'

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)

db = MongoEngine(app) # Enforce our User schema class

# Initiate LoginManager
login_manager = LoginManager(app)
login_manager.login_view = "login"

bcrypt = Bcrypt(app)

# replace "default_value" with your api key if you need to hardcode it
client = MovieClient(os.getenv("OMDB_API_KEY", "default_value"))

from . import routes
