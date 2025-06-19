from flask import Flask
from .config.settings import Config
from .database.core import db, create_all_tables


def create_app() -> Flask:
    """Application factory for the supply chain system."""
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        create_all_tables()

    # Blueprint registration placeholders
    from .auth.routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app
