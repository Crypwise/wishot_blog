from datetime import datetime
from flask import current_app
from flask_login import UserMixin
from wizapp import login_manager
from wizapp import db
import jwt
from time import time


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(50), nullable=False)
    post = db.relationship('Post', backref="author", lazy=True)

    def get_reset_token(self, expires_in=300):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_token(token):
        try:
            user_id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User ('{self.username}', '{self.email}', '{self.password}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    comments = db.Column(db.Integer, default=0)
    categories = db.Column(db.Text, nullable=False)
    image_pic = db.Column(db.String(60), nullable=False, default='image.png')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}', '{self.image_pic}')"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False)
    email = db.Column(db.String(50), nullable=False, unique=False)
    message = db.Column(db.Text, nullable=False)
    post = db.relationship('Post', backref="posts", lazy=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Comment ('{self.name}', '{self.email}', '{self.date_posted}')"
