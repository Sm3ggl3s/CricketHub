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

    def __init__(self, username, name, email,password, pinned_team) -> None:
        self.username = username
        self.name = name
        self.email = email
        self.password = password
        self.pinned_team = pinned_team


