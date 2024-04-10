#!/usr/bin/python3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from podcast_model.model import Base, Country, Region, Category, Podcast
from music_model.music_model import Genre, Music
from user_model.user_model import User

# Create an engine
engine = create_engine('mysql+mysqldb://root:elpastore@localhost:3306/podcast_radio_database')


# Create all tables in the database
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Commit the session
session.commit()
