import os.path

from flask import Flask

def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    from circle.models import db
    db.init_app(app)

    with app.app_context():
        # Add some routes
        if not os.path.exists('circle/drumcircle'):
            db.create_all()
        return app


