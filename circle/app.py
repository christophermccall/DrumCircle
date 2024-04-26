from flask import render_template, request, flash, redirect, url_for
import datetime
from flask_sqlalchemy import SQLAlchemy
# create the instance
from flask_mysqldb import MySQL
from circle.models import Post, db
from . import create_app
import os
#helps flask find all the files in our directory
user = os.environ["user"]
password = os.environ['password']
host = os.environ["host"]
database = os.environ["database"]
port = os.environ["port"]
secretkey = os.environ["secretkey"]
app = create_app()
app.config['SITE_NAME'] = 'Drum Circle'
app.config['SITE_DESCRIPTION'] = 'A community driven learning environment'
app.config['FLASK_DEBUG'] = 1
app.config['MYSQL_HOST'] = host
app.config['MYSQL_USER'] = user
app.config['MYSQL_PASSWORD'] = password
app.config['MYSQL_DB'] = database
app.config['MYSQL_CHARSET'] = 'utf8mb4'

mysql = MySQL(app)
# create a decorator (for connecting routes)








@app.route('/')
def index():
    posts = Post.query.order_by(Post.postID)
    return render_template('index.html', posts=posts)

#{{ url_for('post', post_id=post['id']) }}
@app.route('/index/<int:post_id>')
def post(post_id):
    posts = Post.query.get_or_404(post_id)
    return render_template('blogpost.html', post=posts)


@app.route('/create', methods=('GET', 'POST'))
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

@app.route('/landing')
def landing_page():
    return render_template('landing.html')

with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)