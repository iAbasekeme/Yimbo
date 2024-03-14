from . import db
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Music(db.Model):
    '''A tracks model'''
    __tablename__ = 'Tracks'

    id = mapped_column(Integer, pimary_key=True)
    title = mapped_column(String(60), nullable=False)
    artists_id = mapped_column(Integer, ForeignKey(Artist.id))
    album_id = mapped_column(Integer, ForeignKey(Album.id))
    genre = mapped_column(String(30))
    duration = mapped_column(Time)
    release_year = mapped_column(Integer, nullable=False)
    views = mapped_column(Integer)


with app.app_context():
    db.create_all()
