import os
import bcrypt
from flask.testing import FlaskClient
from flask import session
from src.models import User, db
from tests.utils import create_user, refresh_db

def test_signup_html(test_app: FlaskClient):
    res = test_app.get('/signup')
    page_data = res.data.decode()

    assert res.status_code == 200
    assert '<h2 class="signin-title"> Sign Up </h2>' in page_data


def test_register(test_app: FlaskClient):
    # Setup
    refresh_db()
    test_user = create_user()
    # Action
    res = test_app.post('/register', data={
        'username': 'Tester',
        'fname': 'TestName',
        'email': 'Test@fake.com',
        'password': 'abc'
    }, follow_redirects=True)
    page_data = res.data.decode()
    new_test_user = create_user('Tester1', 'TestName', 'Test@fake.com', 'abc', None)

    if test_user == new_test_user:
        assert res.status_code == 200
        assert len(res.history) == 1
        assert res.request.path == "/signup" 
    else:
        assert res.request.path == "/signup"

def test_register_existing_user(test_app: FlaskClient):
    # Setup
    refresh_db()
    test_user = create_user()

    # Action
    res = test_app.post('/register', data={
        'username': 'Tester',
        'fname': 'TestName',
        'email': 'Test@fake.com',
        'password': 'abc'
    }, follow_redirects=True)


    assert res.status_code == 200
    assert len(res.history) == 1
    assert res.request.path == "/signup" 


def test_register_empty(test_app: FlaskClient):
    # Setup
    refresh_db()

    # Action
    res = test_app.post('/register', data={}, follow_redirects=True)
    page_data = res.data.decode()
    new_test_user = create_user('', '', '', '', None)

    if new_test_user.username == '' or new_test_user.name == '' or new_test_user.email == '' or new_test_user.password == '':
        assert res.status_code == 500
        assert res.request.path == "/register"


def test_login_html(test_app: FlaskClient):
    # Setup
    refresh_db()
    # Action
    res = test_app.get('/login')
    page_data = res.data.decode()

    assert res.status_code == 200
    assert '<h2 class="login-title">Log In</h2>' in page_data

def test_user_login(test_app: FlaskClient):
    # Setup
    refresh_db()
    test_user = create_user()
    
    # Action
    res = test_app.post('/log_in', data={
        'username': 'Tester',
        'fname': 'TestName',
        'email': 'Test@fake.com',
        'password': 'abc'
    }, follow_redirects=True)
    new_test_user = create_user('Tester1', 'TestName', 'Test@fake.com', 'abc', None)

    if new_test_user.password == test_user.password and new_test_user.username == test_user.username:
        assert res.request.path == '/'
        assert len(res.history) == 1
        assert res.status_code == 200



def test_user_login_empty(test_app: FlaskClient):
    # Setup
    refresh_db()
    test_user = create_user()

    # Action
    res = test_app.post('/log_in', data={}, follow_redirects=True)
    new_test_user = create_user('', '', '', '', None)

    if new_test_user.password == test_user.password and new_test_user.username == test_user.username:
        assert res.request.path == '/'
        assert res.status_code == 200
        assert len(res.history) == 1
        assert res.request.path == "/login" 
    


def test_logout(test_app: FlaskClient):
    # Setup
    refresh_db()
    with test_app.session_transaction() as session:
        test_user = create_user()
        
        session['user'] = {
            'user_id': test_user.user_id,
            'username': test_user.username
        }

    # Action
    res = test_app.get('/logout')

    assert len(res.history) == 0
    assert res.request.path == "/logout"