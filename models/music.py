from . import db
from sqlalchemy import create_engine, ForeignKey, DateTime
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
    album = db.relationship('Album', backref="Tracks")
    genre = db.Column(db.String(30), nullable=False)
    duration = db.Column(db.Time)
    release_year = db.Column(db.Integer, nullable=False)
    views = db.Column(db.Integer)

    def __repr__(self):
        return f"{self.title} {self.artist} {self.album}"

with app.app_context():
    db.create_all()
