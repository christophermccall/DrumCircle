import os.path

from flask import Flask, request
from flask_dropzone import Dropzone
from circle.auth import auth
from circle.dashboard import dashboard
from circle.bucket import bucket
def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    app.register_blueprint(bucket)
    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
    from circle.models import db
    db.init_app(app)

    with app.app_context():
        # Add some routes
        if not os.path.exists('circle/drumcircle'):
            db.create_all()
        return app


