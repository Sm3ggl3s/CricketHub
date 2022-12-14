from src.models import *


def refresh_db():
    Comment_dislike.query.delete()
    Comment_like.query.delete()
    Comment.query.delete()
    Team.query.delete()
    Post.query.delete()
    User.query.delete()
    
    db.session.commit()


def create_user(username="Tester", name="Test", email="test@fake.com", password="123", pinned_team=None):
    test_user = User(username=username, name=name, email=email, password=password, pinned_team= pinned_team)
    db.session.add(test_user)
    db.session.commit()
    return test_user


def create_post(post_title="Test Post Title", post_body="Test Post Body", poster_id= 1):
    test_post = Post(post_title=post_title, post_body=post_body, poster_id= poster_id)    
    db.session.add(test_post)
    db.session.commit()
    return test_post

def create_comment(content = "Test Comment Content", post_id= "Test Comment ID", commentor_id = 1):
    test_comment = Comment(content = content, post_id = post_id, commentor_id=commentor_id)
    db.session.add(test_comment)
    db.session.commit()
    return test_comment