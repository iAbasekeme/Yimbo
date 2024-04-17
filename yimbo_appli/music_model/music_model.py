#!/usr/bin/python3
from sqlalchemy import Column, Integer, String, ForeignKey
from yimbo_appli.podcast_model.model import Country, Region, Base
from sqlalchemy.orm import relationship

class Genre(Base):
    """ 
    class Genre: contains a mirror of genre table from podcast_radio db
        args: Base inherited from the model file in the podcast_model module
    """
    __tablename__ = 'genre'
    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    picture = Column(String(255), nullable=False)
    music = relationship('Music', backref='genre')
    
    
    """image_id = Column(Integer, default=0)
    region_id = Column(Integer, ForeignKey('region.id'))
    country_id = Column(Integer, ForeignKey('country.id'))

    # define the relationship between the country, region and radio table
    country = relationship('Country', backref='genre')
    region = relationship('Region', backref='genre')"""
    
class Music(Base):
    """
    class Music: contains a mirror of music table from podcast_radio db
        args: Base inherited from the model file in the podcast_model module"""
    __tablename__ = 'music'
    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    artist_name = Column(String(100), nullable=False)
    duration = Column(String(100), nullable=False) # in format HH:MIN:SS
    genre_id = Column(Integer, ForeignKey('genre.id'))
    music_file = Column(String(250), nullable=False)
    picture = Column(String(250), nullable=False)
