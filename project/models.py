from flask_login import UserMixin
from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(165), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    cif = db.Column(db.String(40), nullable=False)
    timezone = db.Column(db.String(30), nullable=False, default='Europe/Zurich')
    theme = db.Column(db.String(16), nullable=False, default='hootstrap')
    question_count = db.Column(db.Integer, nullable=False, default=0)
    question_max = db.Column(db.Integer, nullable=False, default=0)
    quiz_count = db.Column(db.Integer, nullable=False, default=0)
    quiz_max = db.Column(db.Integer, nullable=False, default=0)
    photo = db.Column(db.String(40), nullable=True)
    avatar = db.Column(db.String(40), nullable=True)