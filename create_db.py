from src.models import db
from app import app

with app.app_context():
    db.create_all()