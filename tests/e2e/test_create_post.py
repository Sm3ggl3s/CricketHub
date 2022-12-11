# from flask import session
# from flask.testing import FlaskClient

# from src.models import Team, User, db,Post
# from tests.utils import refresh_db

# def test_create_post(test_app:FlaskClient):
#     #setup
#     refresh_db()
#     with test_app.session_transaction() as session:
#         test_user = User(username="tester", name='Test', email="test@email.com", password = "abc", pinned_team=None)
#         db.session.add(test_user)
#         db.session.commit()

#         session['user'] = {
#             'user_id': test_user.user_id,
#             'username': test_user.username
#         }
        
#     res = test_app.get('/create_post')
#     page_data = res.data.decode()

#     res2 = test_app.post('/createpost', data={
#         "post_title": "test title",
#         "post_body": "test body",
#     }, follow_redirects=True)


#     assert res.status_code == 200
#     assert len(res2.history) == 1
#     assert res2.request.path == "/"
#     assert '<h2 class="create-title"> Create Post</h2>' in page_data

    

