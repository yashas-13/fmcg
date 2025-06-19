from werkzeug.security import check_password_hash
from ..database.models import User


def authenticate(username: str, password: str) -> User | None:
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        return user
    return None
