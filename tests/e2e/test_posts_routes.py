# from flask.testing import FlaskClient
# from flask import session
# from src.models import Comment, User, Post, db
# from tests.utils import create_post, create_user, refresh_db

# def test_view_post(test_app: FlaskClient):
#     # Setup
#     refresh_db()
#     with test_app.session_transaction() as session:
#         test_user = create_user()
        
#         session['user'] = {
#             'user_id': test_user.user_id,
#             'username': test_user.username
#         }
#     test_post =  create_post(poster_id=session['user']['user_id'])
#     test_comments = Comment.query.filter_by(post_id=test_post.post_id).all()
#     # Action 
#     res = test_app.post(f'/post/{test_post.post_id}', data={
#         'post_id': test_post.post_id
#     }, follow)
#     page_data = res.data.decode()

#     # Asserts
#     assert res.status_code == 200