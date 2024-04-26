from os import path
import os
basedir = path.abspath(path.dirname(__file__))
user = os.environ["user"]
password = os.environ['password']
host = os.environ["host"]
database = os.environ["database"]
port = os.environ["port"]
secretkey = os.environ["secretkey"]
app = os.environ["app"]
class Config:
    """Set Flask configuration from .env file."""
    # General Config
    SECRET_KEY = f'{secretkey}'
    FLASK_APP = app
    # Database
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///drumcircle.db'
    # SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://chrism:{password}@localhost/drumcircle'
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{user}:{password}@{host}/{database}?use_unicode=1&charset=utf8'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False