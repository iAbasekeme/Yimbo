#!/usr/bin/python3
"""podcast model"""
from sqlachemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlachemy.orm import relationship

# create the engine
engine = create_engine('sqlite:///podcast.db', echo=True)

Base = declarative_base()

class PodcastCategory(Base):
    """ create a table for category"""
    __tablename__ = "Category_pod"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    
    # this representation methodis solely for the purpose of debuddng and
    # --understanding the program execution
    def __repr__(self):
        """ print string format of the table"""
        return "Category: {}:{}".format(self.id, self.name)

class Podcast(Base):
    """ create a table for podcast """
    __tablename__ = "Podcast"
    id = Column(Interger, primary_key=True)
    title = Column(String)
    description = Column(string, nullable=False)
    podcast_category = Column(String, nullable=False)
    category_id = (Integer, ForeignKey("category.id"))
    category = relationship("Category", back_populates="podcasts")
    
    # this method is just for debugging and undestanding the process

    def __repr__(self):
        """ print string format of the table"""
        # iterate throuh the Category_pod table
        for pod in podcastCategory.name:
            
            # check if the name is same with podcast_category
            if pod == podcast_category:
                new_podcast_category.append(pod)

            # if the podcast.podcast_category not find in the Category_pod table
            if podcast_category not in PodcastCategory.name:
                print("invalid category name, please provide a valid name")

        return "<Podcast( {} (title= {}, description= {}".format(
                self.podcast_category, self.title, self.descrition)

    Category.podcasts = relationship("Podcast", order_by=Podcast.id, 
    back_populates="category"
    )

# Create tables
Base.meta.create_all(engine)
