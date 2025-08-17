import uuid

import requests
from flask import Flask, url_for
from flask import abort, jsonify, redirect, render_template, request, session
from markupsafe import escape
from pymongo import MongoClient

from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, IntegerField, BooleanField, RadioField)
from wtforms.validators import InputRequired, Length

from flask_sqlalchemy import SQLAlchemy

from pymongo import MongoClient

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
    app.config['TESTING'] = True

    # Enable encrypted session (cookies) so can map user login to CIF, CIF-919ae5a5-34e4-4b88-979a-5187d46d1617
    # Login/password authentication will be via flask-alchemy to MariaDB which will map to CIF
    # CIF is required to get list of Questions, Quizzes and Results
    #  python -c 'import secrets; print(secrets.token_hex())'
    app.config['SECRET_KEY'] = '87ef122423ce0f61e47bddb08e44b347c5cf1fd6a85f7a34162369f4ac4ef999'
    app.config['SESSION_COOKIE_NAME'] = 'flask-play'

    # clean-up: https://pymongo.readthedocs.io/en/stable/examples/authentication.html
    app.config["MONGO_URI"] = "mongodb://root:example@mongo:27017"
    app.config["MONGO_DB"] = "gm01"
    _client = MongoClient(app.config["MONGO_URI"])
    _db = _client[app.config["MONGO_DB"]]

    # blueprint for the Main Web service
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
