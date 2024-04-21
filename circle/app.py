from flask import Flask, render_template
# create the instance
from flask_mysqldb import MySQL
from circle.models import User, db
from . import create_app
#helps flask find all the files in our directory
app = create_app()
app.config['SITE_NAME'] = 'Drum Circle'
app.config['SITE_DESCRIPTION'] = 'A community driven learning environment'
app.config['FLASK_DEBUG'] = 1

mysql = MySQL(app)
# create a decorator (for connecting routes)

@app.route('/')

def index():
    return '<h1>Hello World!<h1>'


with app.app_context():
    db.create_all()
