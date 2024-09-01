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


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
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

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password.encode('utf-8')
        self.bytes = self.password
        self.salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(self.bytes, self.salt) #generate_password_hash(password)

    def check_password(self, password):
        check_bytes = password.encode('utf-8')
        return bcrypt.checkpw(check_bytes, self.password_hash)


class Post(db.Model):
    postID = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    content = db.Column(db.Text)
    caption = db.Column(db.Text)
    postdate = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments = db.relationship("Comment", backref="post")
    exercise = db.relationship("Exercise", backref="post")
    reacts = db.relationship('React', backref="post", lazy="dynamic")

    def __init__(self, title, content, created, caption=None):
        self.title = title
        self.content = content
        self.caption = caption
        self.created = created
        self.last_check = None
        self.saved_response = None


    def get_time_string(self):
        # this only needs to be calculated every so often, not for every request
        # this can be a rudamentary chache
        now = datetime.datetime.now()

        if self.lastcheck is None or (now - self.lastcheck).total_seconds() > 30:
            self.last_check = now
        else:
            return self.saved_response

        diff = now - self.postdate

        seconds = diff.total_seconds()
        print(seconds)
        if seconds / (60 * 60 * 24 * 30) > 1:
            self.saved_response = " " + str(int(seconds / (60 * 60 * 24 * 30))) + " months ago"
        elif seconds / (60 * 60 * 24) > 1:
            self.saved_response = " " + str(int(seconds / (60 * 60 * 24))) + " days ago"
        elif seconds / (60 * 60) > 1:
            self.saved_response = " " + str(int(seconds / (60 * 60))) + " hours ago"
        elif seconds / (60) > 1:
            self.saved_response = " " + str(int(seconds / 60)) + " minutes ago"
        else:
            self.saved_response = "Just a moment ago!"

        return self.saved_response


class Message(db.Model):
    messageID = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    sent = db.Column(db.String(255), nullable=False)
    received = db.Column(db.String(255), nullable=False)
    created = db.Column(db.DateTime)
    exercise = db.relationship("Exercise", backref="message")


class Exercise(db.Model):
    exerciseID = db.Column(db.Integer, primary_key=True)
    exerciseName = db.Column(db.String(255))
    fileName = db.Column(db.String(255))
    bucket = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey("post.postID"))
    message_id = db.Column(db.Integer, db.ForeignKey("message.messageID"))
    audio = db.relationship("Audio", backref="exercise")
    score = db.relationship("Score", backref="exercise")

    def __init__(self,exerciseName, fileName, bucketName):
        self.exerciseName = exerciseName
        self.fileName = fileName
        self.bucket = bucketName



class Audio(db.Model):
    audioID = db.Column(db.Integer, primary_key=True)
    audioName = db.Column(db.String(255))
    fileName = db.Column(db.String(255))
    filePath = db.Column(db.String(255))
    bucket = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercise.exerciseID"))

    def __init__(self, audioName, fileName, bucketName):
        self.audioName = audioName
        self.fileName = fileName
        self.bucket = bucketName

class Comment(db.Model):
    commentID = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255))
    postdate = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey("post.postID"))


class React(db.Model):
    reactID = db.Column(db.Integer, primary_key=True)
    reactType = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey("post.postID"))







class Score(db.Model):
    scoreID = db.Column(db.Integer, primary_key=True)
    attempt = db.Column(db.Integer, default=1)
    score = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.exerciseID'))


