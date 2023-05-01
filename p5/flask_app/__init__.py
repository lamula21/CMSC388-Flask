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
from datetime import datetime
import os

# local
from .client import MovieClient


db = MongoEngine()
login_manager = LoginManager()
bcrypt = Bcrypt()
movie_client = MovieClient(os.environ.get("OMDB_API_KEY"))



# ---------- Project 5 modification ----------


# DONT import this since we already created blueprints
#from .routes import main


# Instead Import the blueprints
from .movies.routes import movies_bp
from .users.routes import users_bp



def page_not_found(e):
    return render_template("404.html"), 404


def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_pyfile("config.py", silent=False)
    if test_config is not None:
        app.config.update(test_config)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    #app.register_blueprint(main)
    
    # Register Blueprint object. Once the blueprint is registered, the view functions will be accessible at the URLs specified by the @users.route decorator.
    app.register_blueprint(movies_bp)
    app.register_blueprint(users_bp)


    app.register_error_handler(404, page_not_found)

    login_manager.login_view = "users_bp.login"

    return app


