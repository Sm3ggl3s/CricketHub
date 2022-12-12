from src.models import * 


def test_team_model():
    test_team = Team(team_info="Test Name")

    assert test_team.team_info == 'Test Name'

def test_favorite_team_model():
    test_favorite_team = favorite_team(user_id=1, team_id=1)

    assert test_favorite_team.user_id == 1
    assert test_favorite_team.team_id == 1

def test_user_model():
    test_user = User(username="Tester", name="Test", email="test@fake.com", password="123", pinned_team=1)

    assert test_user.username == 'Tester'
    assert test_user.name == 'Test'
    assert test_user.email == 'test@fake.com'
    assert test_user.password == '123'
    assert test_user.pinned_team == 1

def test_post_model():
    test_post = Post(post_title="Test Post Title", post_body="Test Post Body", poster_id= 1)

    assert test_post.post_title == 'Test Post Title'
    assert test_post.post_body == 'Test Post Body'
    assert test_post.poster_id == 1

def test_comment_model():
    test_comment = Comment(content="Test Comment", post_id= 1, commentor_id=2)

    assert test_comment.content == 'Test Comment'
    assert test_comment.post_id == 1
    assert test_comment.commentor_id == 2

def post_likes_model():
    test_like = Post_like(post_id=1,users_liked=1)

    assert test_like.post_id == 1
    assert test_like.users_liked == 1

def post_dislikes_model():
    test_dislike = Post_dislike(post_id=1,users_disliked=1)

    assert test_dislike.post_id == 1
    assert test_dislike.users_disliked == 1
