#!/usr/bin/python3
""" models for category and podcasts """

from sqlalchemy import Column, Integer, String
from sqlachemy.ext.declarative import declarative_base

Base = declarative_base()


class Category():
    """ podcast categories for the db"""
    __tablename = "category"
    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)

class Podcast():
    " podcast categories for the db"""
    __tablename = "podcast_category"
    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    description = Column(String(256), nullable=False)
    category_id = Column(Integer, nullable=False)
 
   # id INT NOT NULL AUTO_INCREMENT,
   # name VARCHAR(256) NOT NULL,
   # description VARCHAR NOT NULL
   #  category_id INT NOT NULL,
   #  PRIMARY KEY (id)
   #  FOREIGN KEY(category_id) REFERENCE podcast_category(id)

