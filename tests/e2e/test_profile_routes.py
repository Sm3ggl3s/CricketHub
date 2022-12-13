from flask.testing import FlaskClient
from flask import session
from src.models import User, db
from tests.utils import create_user, refresh_db

def test_profile(test_app: FlaskClient):
    # Setup
    refresh_db()
    with test_app.session_transaction() as session:
        test_user = create_user()
        
        session['user'] = {
            'user_id': test_user.user_id,
            'username': test_user.username
        }

    # Action 
    res = test_app.get(f'/profile/{test_user.user_id}')
    page_data = res.data.decode()


    assert res.status_code == 200
    assert 'Tester' in page_data
    assert 'Test' in page_data
    assert 'test@fake.com' in page_data
    

def test_profile_empty(test_app: FlaskClient):
    # Setup
    refresh_db()
    

    # Action 
    res = test_app.get(f'/profile/')

    assert res.status_code == 404

def test_profile_edit(test_app: FlaskClient):
    # Setup
    refresh_db()
    with test_app.session_transaction() as session:
        test_user = create_user()
        
        session['user'] = {
            'user_id': test_user.user_id,
            'username': test_user.username
        }

    # Action 
    res = test_app.post(f'/update_profile/{test_user.user_id}', data={
        'username': 'Tester1',
        'name': 'TestName',
        'email': 'new@fake.com',
    }, follow_redirects=True)
    page_data = res.data.decode()

    assert res.status_code == 200
    assert test_user.username == 'Tester1' in page_data
    assert res.request.path == f'/update_profile/{test_user.user_id}'