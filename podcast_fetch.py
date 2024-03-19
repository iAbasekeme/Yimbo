#!/usr/bin/python3
"""
Usage:
  ./14-model_city_fetch_by_state.py <mysql_username> <mysql_password>
  <database_name>
"""

from sys import argv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from podcast_model.py import Category, Podcast, Country, Region

if __name__ == "__main__":
  # Connect to the database
  engine = create_engine("mysql+mysqldb://{}:{}@localhost:3306/{}"
                        .format(argv[1], argv[2], argv[3]),
                        pool_pre_ping=True)
  Session = sessionmaker(bind=engine)
  session = Session()

  def print_by_podcast():
    """
    Prints all available podcasts and their descriptions.
    """
    try:
      available_podcasts = session.query(Podcast).all()
      print("Available Podcasts:")

      for podcast in available_podcasts:
        print(f"{podcast.name} : [description: {podcast.description}]")
    except Exception as e:
      print(f"An error occurred while querying podcasts: {e}")

  def print_by_category(category_name):
    """
    Prints podcasts based on the given category name.
    """
    try:
      category = session.query(Category).filter_by(name=category_name).first()

      if category is None:
        print(f"category: {category_name} not found")
        return

      cat_id = category.id
      category_podcasts = session.query(Podcast).filter_by(category_id=cat_id).all()

      if category_podcasts is None:
        print(f"No podcast found in category {category.name}")
        return

      print(f"List of podcasts in {category.name}:")
      for podcast in category_podcasts:
        print(podcast.name)
    except Exception as e:
      print("An error occurred while trying to query the database")


  # Example usage
  if __name__ == "__main__":
    try:
      print_by_podcast()
      print_by_category("Tech & Science")  # Replace with desired category
    except Exception as e:
      print(f"An unexpected error occurred: {e}")

