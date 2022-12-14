from flask.testing import FlaskClient
from flask import session
from src.models import User, Post, db
from tests.utils import create_post, create_user, refresh_db

def test_about_sunny_case(test_app: FlaskClient):
    # Setup
    refresh_db()
    with test_app.session_transaction() as session:
        test_user = create_user()

        session['user'] = {
            'user_id': test_user.user_id,
            'username': test_user.username
        }

    res = test_app.get('/about')
    page_data = res.data.decode()

    assert res.status_code == 200
    assert f'<h3 class="post-header">Behind the <span class="proj">Project</span> </h3>' in page_data
    assert f'<p class="post-details">Hailing from different parts of the world several staunch computer science students gathered together as developers of the next big sports platform. Tasked with the challenge of creating a project that could transform the world. These six astute developers in training analyzed the niche of cricket and its potential to galvanize enthusiasts all around the world and especially in the developers’ nation of operation, the USA. Encouraged by the excitement of the T20 Cricket World Cup 2022 these students joined together to form a site that would not only facilitate a culture for all cricket lovers but in it produce future cricket enthusiasts. A platform where people can be engrossed by cricket culture. Crickethub is the cricket community for everyone!' in page_data 
    assert f'<h3 class="faq-title">FAQs</h3>' in page_data

def test_about_rainy_case(test_app: FlaskClient):
    # Setup
    refresh_db()
    with test_app.session_transaction() as session:
        test_user = create_user()

        session['user'] = {
            'user_id': test_user.user_id,
            'username': test_user.username
        }

    res = test_app.get('/about')
    page_data = res.data.decode()

    assert res.status_code != 500 or res.status_code  != 404
    assert f'<h3 class="post-header"><span class="proj"></span></h3>' not in page_data
    assert f'<p class="post-details"></p>' not in page_data 
    assert f'<h3 class="faq-title"></h3>' not in page_data
