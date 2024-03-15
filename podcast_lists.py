#!/usr/bin/python3
""" models for making new updates to podcast """
from podcast import PodcastCategory, Podcast
from sqlalchemy import sessionmaker
from podcast_main.py import engine

session = sessionmaker(bind=engine)
session = Session()

to_dict = {1: "Tech & Science", 2: "Comedy", 3: "Business/Economics", 4: "Politics", 
           5: "Entertainment/Celebrity Gist"}
def add_new_cat(self):
    for category_name in to_dic.values():
        if not session.query(PodcastCategory).filter_by(
        name=category_name).first():
            session.add(PodcastCategory(name=category_name)
            print(the content of PodcastCategory with its content)

    session.commit()
