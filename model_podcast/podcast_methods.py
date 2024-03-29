#!/usr/bin/python3
"""module for the podcast section"""

from model import Category, Region, Country, Podcast
from podcast_model import get_db
from sqlalchemy import inspect


class PodcastMethods():
    """ the podcast module"""
    def __init__(self, user_name=None):
        self.user_name = user_name

    def get_category(self):
        """Retrieve the category name"""
        with get_db() as db:
            category_data = db.query(Category).all()
            category_info = {}

            for category in category_data:
                category_info[category.id] = {
                    "name": category.name
                }

        return category_info

    def get_region(self):
        """Retrieve the region name"""
        with get_db() as db:
            region_data = db.query(Region).all()
            
            region_info = {}
            for region in region_data:
                region_info[region.id] = {
                    "name": region.name
                }

        return region_info

    def get_country(self):
        """Retrieve the country names and returns a dictionary"""
        print("after get_country main()")
        with get_db() as db:
            country_data = db.query(Country).all()
            country_info = {}
            
            for country in country_data:
                country_info[country.id] = {
                    "name": country.name,
                    "region_id": country.region_id
                }
        return country_info

    def get_table_name(self):
        """Retrieve the table name of the database"""
        with get_db() as db:
            tables_names = inspect(db.get_bind()).get_table_names()

        return tables_names
    
    def get_podcast_info(self):
        """ retrive all infor related to podcast and store in a dictionary"""
        with get_db() as db:
            podcasts = db.query(Podcast).all()
        
            podcast_info = {}
            for podcast in podcasts:
                podcast_info[podcast.id] = {
                    "name": podcast.name,
                    "description": podcast.description,
                    "category_id": podcast.category_id,
                    "region_id": podcast.region_id,
                    "country_id": podcast.country_id
                }   

        return podcast_info

    def category_names(self):
        """returns a list of all categories of podcast"""
        category_info = self.get_category()
        category_names = []
        for cat_id, cat_name in category_info.items():
            category_names.append(cat_name["name"])
        return category_names

    def country_names(self):
         """ display the country name:
                arg: accepts the method country_name
                Retruns: list containing all names of country
         """
         print("after method name")
         country_info = self.get_country()
         print("after get_country()")
         country_names = []
         for country_id, country_name in country_info.items():
            country_names.append(country_name["name"])

         return country_names
    
    def region_names(self):
        """ retrun a list containing the names of all regions"""
        region_info = self.get_region()
        region_names = []
        for region_id, region_name in region_info.items():
            region_names.append(region_name["name"])

        return region_names
    
    def get_podcastsInEachCategory(self, category_name):
        """ retrive all the podcasts in each category """

        # get the id associated with the category_name
        categories = self.get_category()
        if categories:
            for key, value in categories.items():
                if value["name"] == category_name:
                    category_id = key
                    break
        else:
            return None

        # use the category_name id to get the podcast grouped under it
        podcasts = self.get_podcast_info()
        podcasts_in_category = {}
        for key, values in podcasts.items():
            if values["category_id"] == category_id:
                podcasts_in_category[key] = {
                    "name": values["name"],
                    "description": values["description"] 
               }
        return podcasts_in_category

    def get_podcastsInEachRegion(self, region_name):
        """ retrieve all podcast in a region """
        # get the id associated with the region_name
        regions = self.get_region()
        for key, values in regions.items():
             if region_name == values["name"]:
                region_id = key
                break
        
        # use the region id to get the podcast name and description
        podcasts = self.get_podcast_info()
        podcasts_in_region = {}
        for key, values in podcasts.items():
            if values["region_id"] == region_id:
                podcasts_in_region[key] = {
                    "name": values["name"],
                    "description": values["description"]
                }
        return podcasts_in_region
    
    def get_podcastsInEachCountry(self, country_name):
        """ retrieve all podcast in a region """
        country = self.get_country()
        for key, values in country.items():
            if country_name == values["name"]:
                country_id = key
                break
        if country_id == None:
            print("country id not found")
            return None
        
        # use the country id to get the podcast name and description
        podcasts = self.get_podcast_info()
        podcasts_in_country = {}
        for key, values in podcasts.items():
            if values["country_id"] == country_id:
                podcasts_in_country[key] = {
                    "name": values["name"],
                    "description": values["description"]
                }
        return podcasts_in_country
