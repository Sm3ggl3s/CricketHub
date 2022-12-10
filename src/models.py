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
    comments = db.relationship('Comment', backref='commentor')

    def __init__(self, username, name, email,password, pinned_team) -> None:
        self.username = username
        self.name = name
        self.email = email
        self.password = password
        self.pinned_team = pinned_team

class Post(db.Model):
    __tablename__ = 'posts'

    post_id = db.Column(db.Integer, primary_key=True)
    post_title = db.Column(db.String(255), nullable=False)
    post_body = db.Column(db.String(255), nullable=False)
    poster_id = db.Column(db.String, db.ForeignKey('users.user_id'), nullable=False)


    def __init__(self, post_title, post_body, poster_id) -> None:
        self.post_title = post_title
        self.post_body = post_body
        self.poster_id = poster_id
    
    def count_total_likes(self) -> int:
        likes = Post_like.query.filter_by(self.post_id).count()
        dislikes= Post_dislike.query.filter_by(self.post_id).count()
        return likes - dislikes


class Comment(db.Model):
    __tablename__ = 'comments'

    comment_id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String, nullable =False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'), nullable = False)
    commentor_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable = False)

    def __init__(self, content, post_id, commentor_id) -> None:
        self.content = content
        self.post_id = post_id
        self.commentor_id = commentor_id

class Post_like(db.Model):
    __tablename__ = 'post_likes'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'), primary_key=True)
    users_liked = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)


    def __init__(self, post_id, users_liked) -> None:
        self.post_id = post_id
        self.users_liked = users_liked
    
class Post_dislike(db.Model):
    __tablename__= 'post_dislikes'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'), primary_key=True)
    users_disliked= db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)

    def __init__(self, post_id, users_disliked) -> None:
        self.post_id = post_id
        self.users_disliked = users_disliked

class Comment_like(db.Model):
    __tablename__ = 'comment_likes'

    comment_id = db.Column(db.Integer, db.ForeignKey('comments.comment_id'), primary_key=True)
    users_liked = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)

    def __init__(self, comment_id, user_liked) -> None:
        self.comment_id = comment_id
        self.users_liked = user_liked

class Comment_dislike(db.Model):
    __tablename__ = 'comment_dislikes'

    comment_id = db.Column(db.Integer, db.ForeignKey('comments.comment_id'), primary_key=True)
    users_liked = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)

    def __init__(self, comment_id, user_disliked) -> None:
        self.comment_id = comment_id
        self.users_liked = user_disliked