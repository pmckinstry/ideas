"""
Flask Web Application Package

This package contains the main Flask application with authentication
and OAuth support.
"""

import markupsafe
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate

from app.config import config
from app.models import db


def create_app(config_name=None):
    """Application factory pattern"""
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # Load configuration
    if config_name is None:
        config_name = "default"
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "info"

    # Register custom template filters
    @app.template_filter("nl2br")
    def nl2br_filter(text):
        """Convert newlines to HTML line breaks"""
        if text is None:
            return ""
        return markupsafe.Markup(text.replace("\n", "<br>"))

    # Import and register blueprints
    from app.api import api_bp
    from app.auth import auth_bp
    from app.main import main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    # Register user loader
    from app.models import get_user_by_id

    @login_manager.user_loader
    def load_user(user_id):
        return get_user_by_id(user_id)

    # Initialize database and default user
    with app.app_context():
        db.create_all()
        from app.models import init_default_user

        init_default_user()

    return app
