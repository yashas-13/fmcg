from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_all_tables():
    """Create database tables if they do not exist."""
    db.create_all()
