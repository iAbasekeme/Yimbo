#!/usr/bin/python3
""" module that contains a mirror of the radio table from the podcasst_radio db"""
from sqlalchemy import Column, Integer, String, ForeignKey
from podcast_model.model import Country, Region, Base
from sqlalchemy.orm import relationship


class Radio(Base):
    """ 
    class Radio: contains a mirror of radio table from podcast_radio db
        args: Base inherited from the model file in the podcast_model module
    """
    __tablename__ = 'radio'
    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    description = Column(String(1024), nullable=False)
    image_id = Column(Integer, default=0)
    audio_id = Column(Integer)
    picture = Column(String(250), nullable=False)
    region_id = Column(Integer, ForeignKey('region.id'))
    country_id = Column(Integer, ForeignKey('country.id'))

    # define the relationship between the country, region and radio table
    country = relationship('Country', backref='radio')
    region = relationship('Region', backref='radio')
