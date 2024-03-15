from . import db
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, time, DateTime
from sqlalchemy.orm import Column, relationship


class Artist(db.Model):
    '''A artists model'''
    __tablename__ = 'Artist'

    id = Column(Integer, primary_key=True)
    name = Column(String(60), nullable=False)
    about = Column(String(60), nullable=False)
    playlists = relationship('Playlist', back_populates="artist")
    albums = relationship('Album', back_populates="artist")
    tracks = relationship('Tracks', backref="artist")
    subscribers = relationship(
        'User', secondary=ArtistSubscriber, back_populates='subscribed_artists')


with app.app_context():
    db.create_all()
