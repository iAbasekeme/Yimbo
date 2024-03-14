#!/usr/bin/python3
""" models for making new updates to podcast """
from podcast import PodcastCategory, Podcast
from sqlalchemy import sessionmaker

session = sessionmaker(bind=engine)
session = Session()

Category = podCastCategory()

to_dict = {1: Tech/Science, 2: Comedy, 3: Business/Economics, 4:News/Politics, 5:Entertainment/Celebrity Gist}
def add_new_cat(self):
    for category in db loop thouggh the to_dic:
        check if category is in podcastCategory.name if found continue else add it
    tech_cat = Category(name="Tech/Science")
    comedy_cat = Category(name="Comedy")
    business_cat = CAtegory(name="Business/Economics")
    new_cat = Category(name="News/Politics")
    entertainment_category = Category(name="Entertainment/Celebrity Gist")

    
    session.add_all([tech_category, comedy_category, business_category, news_category, 
    entertainment_category]
    )
    session.commit()
