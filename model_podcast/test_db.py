#!/usr/bin/python3

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# Create an engine to connect to the database
engine = create_engine('mysql+mysqldb://root:password@localhost:3306/podcast_database')

# Create a base class for declarative class definitions
Base = declarative_base()

# Define the Region class
class Region(Base):
    __tablename__ = 'region'
    id = Column(Integer, primary_key=True)
    name = Column(String(65), nullable=False)
    countries = relationship('Country', back_populates='region')

# Define the Country class
class Country(Base):
    __tablename__ = 'country'
    id = Column(Integer, primary_key=True)
    name = Column(String(65), nullable=False)
    region_id = Column(Integer, ForeignKey('region.id'))
    region = relationship('Region', back_populates='countries')
    podcasts = relationship('Podcast', back_populates='country')

# Define the Category class
class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    podcasts = relationship('Podcast', back_populates='category')

# Define the Podcast class
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

# Create tables in the database
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Test the connection by querying some data
regions = session.query(Region).all()
for region in regions:
    print(f"Region: {region.name}")
    print("Countries:")
    for country in region.countries:
        print(f"- {country.name}")
        print("Podcasts:")
        for podcast in country.podcasts:
            print(f"  * {podcast.name} - {podcast.description}")
    print("\n")

# Close the session
session.close()
