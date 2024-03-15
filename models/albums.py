from . import db
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, time, DateTime
from sqlalchemy.orm import relationship
from models.artists import Artist



class Album(db.Model):
    '''An album model'''
    __tablename__ = 'Album'

    id = Column(Integer, primary_key=True)
    title = Column(String(60), nullable=False)
    artists_id = Column(Integer, ForeignKey(Artist.id))
    artist = relationship('Artist', back_populates='albums')
    release_date = Column(DateTime)
    views = Column(Integer)
    release_year = Column(DateTime, nullable=False)
    duration = Column(Time)


with app.app_context():
    db.create_all()
