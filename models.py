from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# ვქმნით SQLAlchemy-ს ობიექტს
db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    news = db.relationship('News', backref='author', lazy=True)
   # კავშირი სიახლეებთან
    saved_news = db.relationship('SavedNews', backref='author', lazy=True)


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    image_filename = db.Column(db.String(100))

    # კავშირი მომხმარებელთან
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class SavedNews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    news_id = db.Column(db.Integer, db.ForeignKey('news.id'), nullable=False)