#   from werkzeug.security import generate_password_hash, check_password_hash
#   from flask_bcrypt import Bcrypt
#   import filePath
from flask_login import UserMixin
import datetime
import bcrypt

from flask_login import UserMixin
import datetime
from sqlalchemy import and_

# create db here, so it can be imported (with the models) into the App object.
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

ReactTypes = ['thumbsup']


class User(UserMixin, db.Model):
    userID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True)
    password_hash = db.Column(db.LargeBinary(255))
    email = db.Column(db.String(50), unique=True)
    admin = db.Column(db.Boolean, default=False)
    posts = db.relationship("Post", backref="user")
    comments = db.relationship("Comment", backref="user")
    exercise = db.relationship("Exercise", backref="user")
    audio = db.relationship("Audio", backref="user")
    reacts = db.relationship("React", backref="user", lazy="dynamic")
    messages = db.relationship("Message", backref='user')
    score = db.relationship("Score", backref="user")


class Post(db.Model):
    postID = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    content = db.Column(db.Text)
    postdate = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.userID'))
    comments = db.relationship("Comment", backref="post")
    exercise = db.relationship("Exercise", backref="post")
    reacts = db.relationship('React', backref="post", lazy="dynamic")


class Message(db.Model):
    messageID = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.userID'))
    sent = db.Column(db.String(255), nullable=False)
    received = db.Column(db.String(255), nullable=False)
    created = db.Column(db.DateTime)
    exercise = db.relationship("Exercise", backref="post")


class Exercise(db.Model):
    exerciseID = db.Column(db.Integer, primary_key=True)
    exerciseName = db.Column(db.String(255))
    filePath = db.Column(db.String(255))
    mediaType = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.userID'))
    post_id = db.Column(db.Integer, db.ForeignKey("post.postID"))
    audio = db.relationship("Audio", backref="exercise")
    message = db.relationship("Message", backref="exercise")
    score = db.relationship("Score", backref="exercise")


class Audio(db.Model):
    audioID = db.Column(db.Integer, primary_key=True)
    audioName = db.Column(db.String(255))
    filePath = db.Column(db.String(255))
    mediaType = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.userID'))
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercise.exerciseID"))


class Comment(db.Model):
    commentID = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255))
    postdate = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.userID'))
    post_id = db.Column(db.Integer, db.ForeignKey("post.postID"))


class React(db.Model):
    reactID = db.Column(db.Integer, primary_key=True)
    reactType = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.userID'))
    post_id = db.Column(db.Integer, db.ForeignKey("post.postID"))


class Score(db.Model):
    scoreID = db.Column(db.Integer, primary_key=True)
    attempt = db.Column(db.Integer, default=1)
    score = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.userID'))
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.exerciseID'))
