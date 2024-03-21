#!/usr/bin/python3
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# Database connection details (replace with yours)
DATABASE_URI = "mysql+pymysql://my_username:my_password@localhost:3306/podcast_database"

engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)

    podcasts = relationship("Podcast", backref="category")

class Region(Base):
    __tablename__ = "Region"
    id = Column(Integer, primary_key=True)
    name = Column(String(65), nullable=False)

    countries = relationship("Country", backref="region")

class Country(Base):
    __tablename__ = "country"
    id = Column(Integer, primary_key=True)
    name = Column(String(65), nullable=False)
    region_id = Column(Integer, ForeignKey("Region.id"), nullable=False)

    podcasts = relationship("Podcast", backref="country")

class Podcast(Base):
    __tablename__ = "podcast"
    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    description = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)
    region_id = Column(Integer, ForeignKey("Region.id"), nullable=False)
    country_id = Column(Integer, ForeignKey("country.id"), nullable=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    Base.metadata.create_all(engine)
