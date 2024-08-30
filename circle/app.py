from flask import render_template, request, flash, redirect, url_for, session
from flask_login import LoginManager, current_user, login_required, logout_user
from circle.models import User, Exercise, Audio
import datetime
import boto3
from flask_sqlalchemy import SQLAlchemy
# create the instance
from flask_mysqldb import MySQL
from circle.models import Post, db
from . import create_app
from config import Config

app = create_app()
app.config.from_object(Config)

mysql = MySQL(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


s3 = boto3.client('s3')
bucket_name = 'drum-circle-app-bucket-2'
location = {'LocationConstraint': 'us-east-2'}
response = s3.list_objects(Bucket=bucket_name)
for object in response['Contents']:
    print(object['Key'])


# create a decorator (for connecting routes)
@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))


@app.route('/login')
def login():
    return render_template("landing.html")


# @app.route('/logout', methods=['GET', 'POST'])
# def logout():
#     logout_user()
#     return redirect(url_for('/'))


@app.route('/')
@login_required
def index():
    urls = []
    audio_urls = []

    exercises = Exercise.query.order_by(Exercise.exerciseID)

    # exercise = Exercise.query.filter_by(user_id=current_user.id).first()
    for exercise in exercises:
        url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': bucket_name,
                    'Key': exercise.fileName,
                    'ResponseContentType': 'application/pdf',
                    'ResponseContentDisposition': 'inline; filename="{}"'.format(exercise.fileName)},
            ExpiresIn=3608)
        audio = Audio.query.filter_by(exercise_id=exercise.exerciseID)
        audio_url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': bucket_name,
                    'Key': audio.fileName,
                    'ResponseContentType': 'audio/mpeg'},
            ExpiresIn=3608)
        audio_urls.append(audio_url)
        urls.append(url)
    return render_template('dashboard.html', urls=urls, audio_urls=audio_urls)





#{{ url_for('post', post_id=post['id']) }}
# @app.route('/index/<int:post_id>')
# @login_required
# def post(post_id):
#     posts = Post.query.get_or_404(post_id)
#     return render_template('blogpost.html', post=posts)
#
#
# @app.route('/create', methods=('GET', 'POST'))
# @login_required
# def create():
#     if request.method == 'POST':
#         title = request.form['title']
#         content = request.form['content']
#         entry = Post(title, content, datetime.datetime.now())
#         if not title:
#             flash('Title is required!')
#         else:
#             db.session.add(entry)
#             db.session.commit()
#             return redirect('/')
#     return render_template('createblogpost.html')
#
#
#
#
# @app.route('/edit/<int:post_id>', methods=('GET', 'POST'))
# @login_required
# def edit(post_id):
#     post = Post.query.get_or_404(post_id)
#     if request.method == 'POST':
#         title = request.form['title']
#         content = request.form['content']
#         entry = Post(title, content, datetime.datetime.now())
#         if not title:
#             flash('Title is required!')
#         else:
#             post.title = title
#             post.content = content
#             post.created = datetime.datetime.now()
#             db.session.add(post)
#             db.session.commit()
#         return redirect('/')
#
#     return render_template('edit.html', post=post)
#
#
# @app.route('/index/delete/<int:post_id>/', methods=('POST', 'GET'))
# @login_required
# def delete(post_id):
#     post_to_delete = Post.query.get_or_404(post_id)
#     try:
#         db.session.delete(post_to_delete)
#         db.session.commit()
#         flash("Entry Deleted")
#         return redirect('/')
#     except:
#         return redirect('/')
#     # get_db_connection()
#     # my_cursor.execute('DELETE FROM Post WHERE id = %d', (id,))
#     # mydb.commit()
#     # flash('"{}" was successfully deleted!'.format(post['title']))
#
#
#
#
#
#
#
#
#
# with app.app_context():
#     db.create_all()


