#!/usr/bin/python3
from sys import argv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from podcast_model.py import PodcastCategory, Podcast


if __name__ == "__main__":
    engine = create_engine("mysql+mysqldb://{}:{}@localhost:3306/{}"
                           .format(argv[1], argv[2], argv[3]),
                           pool_pre_ping=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    for podcast, podcast_cat in session.query(Podcast, Category) \
                              .filter(Podcast.category_id == Category.id) \
                              .order_by(Podcast.id):
        print("{}: ({}) {}".format(Category.name, Podcast.id, Podcast.name))
