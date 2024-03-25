#!/usr/bin/python3

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Region(Base):
    __tablename__ = 'region'
    id = Column(Integer, primary_key=True)
    name = Column(String(65), nullable=False)
    countries = relationship('Country', back_populates='region')

class Country(Base):
    __tablename__ = 'country'
    id = Column(Integer, primary_key=True)
    name = Column(String(65), nullable=False)
    region_id = Column(Integer, ForeignKey('region.id'))
    region = relationship('Region', back_populates='countries')
    podcasts = relationship('Podcast', back_populates='country')

class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    podcasts = relationship('Podcast', back_populates='category')

class Podcast(Base):
    __tablename__ = 'podcast'
    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    description = Column(String(1024), nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'))
    region_id = Column(Integer, ForeignKey('region.id'))
    country_id = Column(Integer, ForeignKey('country.id'))
    category = relationship('Category', back_populates='podcasts')
    country = relationship('Country', back_populates='podcasts')
