import os
from flask import redirect, request, session, Blueprint

from src.models import db, User
from security import bcrypt

router = Blueprint('session', __name__)

@router.post('/register')
def register():
    username = request.form.get('username')
    name = request.form.get('fname')
    email = request.form.get('email')
    password = request.form.get('password')
    pinned_team = None

    # Making sure username is unique
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return redirect('/signup')

    # Salt and hash password
    hashed_password = bcrypt.generate_password_hash(password, int(os.getenv('BCRYPT_ROUNDS'))).decode('utf-8') 

    # Save user
    new_user = User(username, name, email, hashed_password, pinned_team)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/')

@router.post('/log_in')
def user_login():
    username = request.form.get('username')
    password = request.form.get('password')

    existing_user = User.query.filter_by(username=username).first()
    if not existing_user:
        return redirect('/')

    if not bcrypt.check_password_hash(existing_user.password, password):
        return redirect('/')

    session['user'] = {
        'user_id': existing_user.user_id,
        'username': existing_user.username
    }

    return redirect('/')

@router.post('/logout')
def logout():
    session.pop('user')
    
    return redirect('/login')
