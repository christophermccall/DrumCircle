from flask import render_template, Blueprint
from flask_login import LoginManager, current_user, login_required
from circle.models import User, Score, Exercise, Audio, db
dashboard = Blueprint('dashboard', __name__, template_folder='templates')

@dashboard.route('/dashboard')
@login_required
def dash():
    return render_template('dashboard.html')

