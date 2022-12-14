from flask.testing import FlaskClient
from src.models import *

from tests.utils import *

def test_single_posts(test_app: FlaskClient):
    #setup
    # Setup
    refresh_db()
    with test_app.session_transaction() as session:
        test_user = create_user()

        session['user'] = {
            'user_id': test_user.user_id,
            'username': test_user.username
        }
    test_post =  create_post(poster_id=session['user']['user_id'])

    #run action
    res = test_app.get(f'/post/{test_post.post_id}')
    page_data: str = res.data.decode()

    #asserts
    assert res.status_code == 200
    assert '<h3 class="post-title p-2"> Test Post Title </h3>' in page_data
    assert '<p class="post-details">Test Post Body</p>' in page_data
    assert f'<p class="post-by"> Posted By: <span> {test_user.username} </span> </p>' in page_data
   

def test_single_post_404(test_app: FlaskClient):
    #setup
    refresh_db()

    #runaction
    res = test_app.get('/post')

    #assert 
    assert res.status_code ==404

def test_post_create(test_app: FlaskClient):
    #setup
    refresh_db()
    with test_app.session_transaction() as session:
        test_user = create_user()

        session['user'] = {
            'user_id': test_user.user_id,
            'username': test_user.username
        }
    poster_id=session['user']['user_id']
    #run action
    res = test_app.post('/createpost', data={
        'post_title': 'Test Post Title',
        'post_body': 'Test Post Body',
        'poster_id': poster_id,
    }, follow_redirects = True)
    page_data = res.data.decode()

    #asserts
    assert res.status_code==200
    assert '<h3 class="post-title p-2"> Test Post Title </h3>' in page_data
    assert '<p class="post-details"> Test Post Body</p>' in page_data
    assert f'<p class="post-by"> Posted By: <span> {test_user.username} </span> </p>' in page_data

def test_create_post_400(test_app: FlaskClient):
    #setup
    refresh_db()
    with test_app.session_transaction() as session:
        test_user = create_user()

        session['user'] = {
            'user_id': test_user.user_id,
            'username': test_user.username
        }
    poster_id=session['user']['user_id']
    
    #run action
    res=test_app.post('/createpost', data={}, follow_redirects=True)

    #asserts
    assert res.status_code == 400

def test_all_comments(test_app: FlaskClient):
    #setup
    refresh_db()
    with test_app.session_transaction() as session:
        test_user = create_user()

        session['user'] = {
            'user_id': test_user.user_id,
            'username': test_user.username
        }
    poster_id=session['user']['user_id']

    #run action
    test_post =  create_post(poster_id=session['user']['user_id'])