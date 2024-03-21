from . import db
from sqlalchemy import create_engine, ForeignKey, DateTime, Interval
# from models.artists import artists
from models.albums import Album


class Music(db.Model):
    '''A tracks model'''
    __tablename__ = 'Tracks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), nullable=False)
    artists_id = db.Column(db.Integer, db.ForeignKey('artists.id'))
    artist = db.relationship('artists', back_populates='tracks')
    album_id = db.Column(db.Integer, db.ForeignKey('albums.id'))
    album = db.relationship('Album', back_populates='tracks')
    genre = db.Column(db.String(30), nullable=False)
    duration = db.Column(Interval)
    release_year = db.Column(db.Integer, nullable=False)
    views = db.Column(db.Integer)

    def __repr__(self):
        return f"{self.title} {self.artist} {self.album}"

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'artist': self.artist,
            'album': self.album.title if self.album else None,
            'genre': self.genre,
            'duration': str(self.duration) if self.duration else None,
            'release_year': self.release_year,
            'views': self.views
        }

with app.app_context():
    db.create_all()
