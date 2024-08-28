from flask import render_template, request, flash, redirect, url_for, session
from flask_login import LoginManager, current_user, login_required, logout_user
from circle.models import User
import datetime

from flask_sqlalchemy import SQLAlchemy
# create the instance
from flask_mysqldb import MySQL
from circle.models import Post, db
from . import create_app
from config import Config  # Import your Config class

app = create_app()
app.config.from_object(Config)  # Load configuration from Config class

mysql = MySQL(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


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
    posts = Post.query.order_by(Post.postID)
    return render_template('index.html', posts=posts)





#{{ url_for('post', post_id=post['id']) }}
@app.route('/index/<int:post_id>')
@login_required
def post(post_id):
    posts = Post.query.get_or_404(post_id)
    return render_template('blogpost.html', post=posts)


@app.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        entry = Post(title, content, datetime.datetime.now())
        if not title:
            flash('Title is required!')
        else:
            db.session.add(entry)
            db.session.commit()
            return redirect('/')
    return render_template('createblogpost.html')




@app.route('/edit/<int:post_id>', methods=('GET', 'POST'))
@login_required
def edit(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        entry = Post(title, content, datetime.datetime.now())
        if not title:
            flash('Title is required!')
        else:
            post.title = title
            post.content = content
            post.created = datetime.datetime.now()
            db.session.add(post)
            db.session.commit()
        return redirect('/')

    return render_template('edit.html', post=post)


@app.route('/index/delete/<int:post_id>/', methods=('POST', 'GET'))
@login_required
def delete(post_id):
    post_to_delete = Post.query.get_or_404(post_id)
    try:
        db.session.delete(post_to_delete)
        db.session.commit()
        flash("Entry Deleted")
        return redirect('/')
    except:
        return redirect('/')
    # get_db_connection()
    # my_cursor.execute('DELETE FROM Post WHERE id = %d', (id,))
    # mydb.commit()
    # flash('"{}" was successfully deleted!'.format(post['title']))









with app.app_context():
    db.create_all()


