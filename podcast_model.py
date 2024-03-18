#!/usr/bin/python3
""" models for category and podcasts """

from sqlalchemy import create_engine, Column, Integer, String, Foreignkey
from sqlachemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Category(Base):
    """ podcast categories for the db"""
    __tablename = "category"
    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)

class Region(Base):
    """podcast based on region for the db"""
    __tablename__ = "Region"
    id = Column(Integer, primary_key=True)
    name = Column(string(65), nullable=False)

class Country(Base):
    """country table"""
    __tablename__ = "country"
    id = Column(Integer, primary_key=True)
    name = Column(String(65), nullable=False)
    region_id = Column(Integer, ForeignKey(Region.id), nullable=False)

class Podcast(Base):
    " podcast categories for the db"""
    __tablename = "podcast"
    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    description = Column(String(256), nullable=False)
    category_id = Column(Integer, ForeignKey(category.id), (nullable=False)
    country_id = Column(Integer, ForeignKey(country.id), nullable=False)
    region_id = Column(Integer, ForeignKey(Region.id), nullable=False)

 
   # id INT NOT NULL AUTO_INCREMENT,
   # name VARCHAR(256) NOT NULL,
   # description VARCHAR NOT NULL
   #  category_id INT NOT NULL,
   #  PRIMARY KEY (id)
   #  FOREIGN KEY(category_id) REFERENCE podcast_category(id)

