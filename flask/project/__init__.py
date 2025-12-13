# import uuid
from datetime import timedelta

from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient

# import requests
from flask import Flask, url_for
from flask import abort, jsonify, redirect, render_template, request, session

# from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
# from markupsafe import escape
# from pymongo import MongoClient
# from flask_wtf import FlaskForm
# from wtforms import (StringField, TextAreaField, IntegerField, BooleanField, RadioField)
# from wtforms.validators import InputRequired, Length

mongo_database_config = {
    "MONGO_URI": "mongodb://root:example@mongo:27017",
    "DATA": "gmdata",
    "IMAGES": "gmimages"
}
mongo_client = MongoClient(mongo_database_config["MONGO_URI"])
mongo_data = mongo_client[mongo_database_config["DATA"]]
mongo_images = mongo_client[mongo_database_config["IMAGES"]]

db = SQLAlchemy()  # init SQLAlchemy so we can use it later in our models


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    # flask config: https://flask.palletsprojects.com/en/stable/config/
    # https://flask.palletsprojects.com/en/stable/config/#builtin-configuration-values
    app.config['TESTING'] = True

    # Enable encrypted session (cookies) so can map user login to CIF, CIF-919ae5a5-34e4-4b88-979a-5187d46d1617
    # Login/password authentication will be via flask-alchemy to MariaDB which will map to CIF
    # CIF is required to get list of Questions, Quizzes and Results
    #  python -c 'import secrets; print(secrets.token_hex())'
    app.config['SECRET_KEY'] = '04816d50aa194cdfc066a450a96c30fc59ef538e4c7bd32b710a15f06cba58ff'
    app.config['SESSION_COOKIE_NAME'] = 'flask-play'
    # app.config['SESSION_COOKIE_SECURE'] = True # HTTPS only
    app.config['SESSION_COOKIE_HTTPONLY'] = True # No JavaScript access
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_USE_SIGNER'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mariadb+pymysql://root:example@authdb/auth?charset=utf8mb4'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg://root:example@postgres/auth'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+pg8000://root:example@postgres/auth'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.jinja_env.lstrip_blocks = True
    app.jinja_env.trim_blocks = True

    # clean-up: https://pymongo.readthedocs.io/en/stable/examples/authentication.html
    app.config["MONGO_URI"] = "mongodb://root:example@mongo:27017"
    app.config["MONGO_DB"] = "gm01"
    _client = MongoClient(app.config["MONGO_URI"])
    _db = _client[app.config["MONGO_DB"]]

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for the Main Web service
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # blueprint for the flask diagnostics
    from .diagnostics import diagnostics as diagnostics_blueprint
    app.register_blueprint(diagnostics_blueprint)

    return app
