#!/usr/bin/python3
"""podcast model"""
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import ProgrammingError
from sqlalchemy import inspect

# Create engine and session
engine = create_engine('sqlite:///podcast_database.db')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


# Define the Podcast model
class Podcast(Base):
    __tablename__ = 'podcast'

    category_id = Column(Integer, primary_key=True)
    category_name = Column(String(255), primary_key=True)
    podcast_name = Column(String(255), primary_key=True)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return "<Podcast(category='{0}', name='{1}')>".format(self.category_name, self.podcast_name)


# Check if the database exists
def check_database_exists():
    insp = inspect(engine)
    return insp.has_table('podcast')

# Check if the table exists
def check_table_exists():
    insp = inspect(engine)
    return insp.has_table('podcast')

# Method to print podcasts based on category
def print_podcasts_by_category(category):
    podcasts = session.query(Podcast).filter_by(category_name=category).all()
    if podcasts:
        print("Podcasts in category '{}':".format(category))
        for podcast in podcasts:
            print("- {}: {}".format(podcast.podcast_name, podcast.description))
    else:
        print("No podcasts found in category '{}'.".format(category))


# Method to add a new podcast to a category in the database
def add_podcast_to_category(category_id, category_name, podcast_name, description):
    new_podcast = Podcast(category_id=category_id, category_name=category_name,
                          podcast_name=podcast_name, description=description)
    session.add(new_podcast)
    session.commit()


# Method to delete a podcast from a category
def delete_podcast_from_category(podcast_name, category_name):
    podcast_to_delete = session.query(Podcast).filter_by\
                        (podcast_name=podcast_name, category_name=category_name).first()
    if podcast_to_delete:
        session.delete(podcast_to_delete)
        session.commit()
        print("Podcast '{}' deleted from category '{}'.".format(
               podcast_name, category_name))
    else:
        print("Podcast '{}' not found in category '{}'.".format(
               podcast_name, category_name))


if __name__ == "__main__":
    # Check if the database exists
    if not check_database_exists():
        print("Database does not exist.")
    else:
        # Check if the table exists
        if not check_table_exists():
            print("Table 'podcast' does not exist.")
        else:
            # Example usage
            # Print podcasts in the 'Tech/Science' category
            print_podcasts_by_category('Tech/Science')

            # Add a new podcast to the 'Tech/Science' category
            add_podcast_to_category(1, 'Tech/Science', 'New Tech Podcast', 'Description of the new tech podcast.')

            # Print podcasts in the 'Tech/Science' category after adding the new podcast
            print_podcasts_by_category('Tech/Science')

            # Delete a podcast from a category
            delete_podcast_from_category('Reply All', 'Tech/Science')

            # Print podcasts in the 'Tech/Science' category after deleting the podcast
            print_podcasts_by_category('Tech/Science')
