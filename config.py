from os import path
import os
import urllib.parse

# Encode the password using UTF-8

basedir = path.abspath(path.dirname(__file__))
user = os.environ["user"]
password = os.environ['password']
host = os.environ["host"]
database = os.environ["database"]
port = os.environ["port"]
secretkey = os.environ["secretkey"]
app = os.environ["app"]
class Config:
    SECRET_KEY = f'{secretkey}'
    FLASK_APP = app
    # Database
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///drumcircle.db'
    # SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://chrism:{password}@localhost/drumcircle'
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{user}@{host}:{port}/{database}?charset=utf8mb4'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # commit test 2