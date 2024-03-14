from . import db
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, time, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Album(db.Model):
    '''An album model'''
    __tablename__ = 'Album'

    id = mapped_column(Integer, primary_key=True)
    title = mapped_column(String(60), nullable=False)
    artists_id = mapped_column(Integer, ForeignKey(Artist.id))
    release_date = mapped_column(Date)
    views = mapped_column(Integer)
    release_year = mapped_column(DateTime, nullable=False)
    duration = mapped_column(Time)


with app.app_context():
    db.create_all()
