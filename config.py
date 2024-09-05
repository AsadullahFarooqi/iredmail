# config.py
import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'mysql+pymysql://user:password@localhost/iredmail')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Mailbox(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Forwarding(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source_email = db.Column(db.String(120), nullable=False)
    destination_email = db.Column(db.String(120), nullable=False)

class Domain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    domain_name = db.Column(db.String(120), unique=True, nullable=False)