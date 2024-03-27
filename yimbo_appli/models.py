#!/usr/bin/python3
from datetime import datetime
from yimbo_appli import db, login_manager
from flask_login import UserMixin
from time import time
import jwt
from yimbo_appli import app

@login_manager.user_loader
def load_user(user_id):
    """
    handle user login
    """
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # image_file = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    
    def get_reset_token(self, expires=600):
        """
        generate a token
        """
        return jwt.encode({'reset_password': self.username, 'exp': time() + expires}, app.config['SECRET_KEY'], algorithm='HS256')
    
    @staticmethod
    def verify_reset_token(token):
        """
        check if token is valid
        """
        try:
            username = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return None
        return User.query.filter_by(username=username).first()
    
    def __repr__(self):
        return f"User('{self.username}',' {self.email}')"
