from flask.testing import FlaskClient
from flask import session
from src.models import User, Post, db
from tests.utils import create_post, create_user, refresh_db
#Main Page Test
def test_index(test_app: FlaskClient):
    # Setup
    refresh_db()
    with test_app.session_transaction() as session:
        test_user = create_user()
        
        session['user'] = {
            'user_id': test_user.user_id,
            'username': test_user.username
        }
    test_post =  create_post(poster_id=session['user']['user_id'])
    # Action
    res = test_app.get('/')
    page_data = res.data.decode()

    # Asserts
    assert res.status_code == 200
    assert '<h3 class="post-title p-2"> Test Post Title </h3>' in page_data
    assert '<p class="post-details"> Test Post Body</p>' in page_data
    assert f'<p class="post-by"> Posted By: <span> {test_user.username} </span> </p>' in page_data
#Main page test with no posts
def test_index_no_post(test_app: FlaskClient):
    # Setup
    refresh_db()
    with test_app.session_transaction() as session:
        test_user = create_user()
        
        session['user'] = {
            'user_id': test_user.user_id,
            'username': test_user.username
        }
    
    # Action
    res = test_app.get('/')
    page_data = res.data.decode()

    assert res.status_code == 200
    assert ' <div class="container user-post box-outline">' not in page_data