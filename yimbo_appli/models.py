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
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
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

class Music(db.Model):
    __tablename__ = 'music'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.String(20), nullable=False)
    picture = db.Column(db.String(100), nullable=False, default='default.jpg')
    music_file = db.Column(db.String(100), nullable=False)
    likes = db.relationship('Like', backref='song', cascade="delete")

    def __repr__(self):
        return f"Music(title='{self.title}', artist='{self.artist}', duration='{self.duration}')"


class Like(db.Model):
    '''A like model'''
    __tablename__ = 'Likes'
    id = db.Column(db.Integer, primary_key=True)
    song_ids = db.Column(db.Integer, ForeignKey(
        'music.id'), primary_key=True)
    user_ids = db.Column(db.Integer, ForeignKey('user.id'), primary_key=True)


class Playlist(db.Model):
    '''A playlist model'''
    __tablename__ = 'playlists'

    id = db.Column(db.Integer, Primary_key=True)
    title = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(60), nullable=True)
    image = db.Column(db.String())
    songs = relationship(
        "Music", secondary=playlist_tracks, backref="playlists", cascade="delete")

    def __repr__(self):
        return f"Playlist name is {self.title}"


class playlist_tracks(db.Model):
    '''A table for playlist_tracks'''
    __tablename__ = 'playlist_tracks'

    playlist_id = db.Column(db.Integer, ForeignKey(
        'playlists.id'), primary_key=True)
    track_id = db.Column(db.Integer, ForeignKey('music.id', primary_key=True))
    sequence_number = db.Column(db.Integer, unique=True)
