from . import db
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Time, DateTime
from sqlalchemy.orm import Column, relationship
from models.artists import Artist
from models.albums import Album


class Music(db.Model):
    '''A tracks model'''
    __tablename__ = 'Tracks'

    id = Column(Integer, pimary_key=True)
    title = Column(String(60), nullable=False)
    artists_id = Column(Integer, ForeignKey(Artist.id))
    artist = relationship('Artist')
    album_id = Column(Integer, ForeignKey(Album.id))
    genre = Column(String(30))
    duration = Column(Time)
    release_year = Column(DateTime, nullable=False)
    views = Column(Integer)


with app.app_context():
    db.create_all()
