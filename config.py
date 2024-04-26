from os import path
from env import key
basedir = path.abspath(path.dirname(__file__))

class Config:
    """Set Flask configuration from .env file."""
    # General Config
    SECRET_KEY = f'{input('secret key')}'
    FLASK_APP = 'circle.app'
    # Database
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///drumcircle.db'
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://chrism:{input('db password')}@localhost/drumcircle'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False