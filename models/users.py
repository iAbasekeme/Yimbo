#!/usr/bin/python3
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(60), nullable=False, unique=True)
    last_name = Column(String(60), nullable=False, unique=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(60), nullable=False, unique=True)
    password = Column(String(128), nullable=False, unique=True)
    birthday = Column(Date, nullable=False)
    phone_number =  Column(Integer, nullable=True) # Optional