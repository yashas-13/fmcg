from flask import Blueprint, request, session, redirect, url_for
from werkzeug.security import generate_password_hash
from ..database.core import db
from ..database.models import User
from .service import authenticate

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = authenticate(username, password)
        if user:
            session['user_id'] = user.id
            session['role'] = user.role
            return redirect(url_for('auth.dashboard'))
    return 'Login Page'


@auth_bp.route('/dashboard')
def dashboard():
    return 'Dashboard'


@auth_bp.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    role = request.form.get('role', 'manufacturer')
    user = User(username=username, password=generate_password_hash(password), role=role)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('auth.login'))
