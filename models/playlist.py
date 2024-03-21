''' A package that holds the playlist of an artist'''
from . import db
from sqlalchemy import Interval


class Playlist(db.Model):
    '''A playlist model'''
    __tablename__ = 'playlists'

    id = db.Column(db.Integer, Primary_key=True)
    title = db.Column(db.String(60), nullable=False)
    about = db.Column(db.String(60), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))
    image = db.Column(db.Integer, )
    # tracks = db.relationship('Music')


class playlist_tracks(db.Model):
    '''A table for playlist_tracks'''
    __tablename__ = 'playlist_tracks'

    playlist_id = db.Column(db.Integer, ForeignKey(
        'playlists.id'), primary_key=True)
    track_id = db.Column(db.Integer, ForeignKey('tracks.id', primary_key=True))
    playlist = db.relationship('Playlist', back_populates='Tracks')
    track = db.relationship('Music', back_populates='playlists')
