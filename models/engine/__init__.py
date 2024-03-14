from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    '''Subclass for all classes'''
    pass


'''db object using the SQLAlchemy constructor.'''
db = SQLAlchemy(model_class=Base)
