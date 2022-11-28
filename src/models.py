from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    pinned_team = db.Column(db.Integer, nullable=True)
    posts = db.relationship('Post', backref='poster')

    def __init__(self, username, name, email,password, pinned_team) -> None:
        self.username = username
        self.name = name
        self.email = email
        self.password = password
        self.pinned_team = pinned_team

class Post(db.Model):
    __tablename__ = 'posts'

    post_id = db.Column(db.Integer, primary_key=True)
    likes = db.Column(db.Integer, nullable=True)
    dislikes = db.Column(db.Integer, nullable=True)
    post_title = db.Column(db.String, nullable=False)
    post_body = db.Column(db.String, nullable=False)
    poster_id = db.Column(db.String, db.ForeignKey('users.user_id'), \
    nullable=False)

    def __init__(self, post_title, post_body, poster_id) -> None:
        self.post_title = post_title
        self.post_body = post_body
        self.poster_id = poster_id

class Comment(db.Model):
    __tablename__ = 'comments'

    comment_id = db.Column(db.Integer, primary_key = True)
    likes = db.Column(db.Integer, nullable=True)
    dislikes = db.Column(db.Integer, nullable=True)
    content = db.Column(db.String, nullable =False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'), nullable = False)
    commentor_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable = True)

    def __init__(self, comment_id, content, post_id) -> None:
        self.comment_id = comment_id
        self.content = content
        self.post_id = post_id