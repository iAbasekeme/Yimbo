#!/usr/bin/python3

from .model import Category, Region, Country, Podcast
from .podcast_model import get_db
from sqlalchemy import inspect
# from PIL import Image
import os


class PodcastMethods():
    """The podcast module"""
    def __init__(self, name=None, description=None, category_id=None, region_id=None, country_id=None):
        self.name = name
        self.description = description
        self.category_id = category_id
        self.region_id = region_id
        self.country_id = country_id
        self.image_id = None

    def create_podcast(self):
        """Create a new podcast"""
        with get_db() as db:
            new_podcast = Podcast(name=self.name, description=self.description, category_id=self.category_id,
                                  region_id=self.region_id, country_id=self.country_id, image_id=self.image_id)
            db.add(new_podcast)
            db.commit()

            # Set image_id to the id of the newly created podcast
            new_podcast.image_id = new_podcast.id
            db.commit()

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
        """Retrieve all info related to podcast and store in a dictionary"""
        with get_db() as db:
            podcasts = db.query(Podcast).all()
        
            podcast_info = {}
            for podcast in podcasts:
                podcast_info[podcast.id] = {
                    "name": podcast.name,
                    "description": podcast.description,
                    "category_id": podcast.category_id,
                    "region_id": podcast.region_id,
                    "country_id": podcast.country_id,
                    "image_id": podcast.image_id
                }   

        return podcast_info

    def category_names(self):
        """Returns a list of all categories of podcast"""
        category_info = self.get_category()
        category_names = []
        for cat_id, cat_name in category_info.items():
            category_names.append(cat_name["name"])
        return category_names

    def country_names(self):
         """Display the country name:
                Arg: accepts the method country_name
                Returns: list containing all names of country
         """
         print("After method name")
         country_info = self.get_country()
         print("After get_country()")
         country_names = []
         for country_id, country_name in country_info.items():
            country_names.append(country_name["name"])

         return country_names
    
    def region_names(self):
        """Return a list containing the names of all regions"""
        region_info = self.get_region()
        region_names = []
        for region_id, region_name in region_info.items():
            region_names.append(region_name["name"])

        return region_names
    
    def get_podcastsInEachCategory(self, category_name):
        """Retrieve all the podcasts in each category"""

        # Get the id associated with the category_name
        categories = self.get_category()
        if categories:
            for key, value in categories.items():
                if value["name"] == category_name:
                    category_id = key
                    break
        else:
            return None

        # Use the category_name id to get the podcast grouped under it
        podcasts = self.get_podcast_info()
        podcasts_in_category = {}
        for key, values in podcasts.items():
            if values["category_id"] == category_id:
                podcasts_in_category[key] = {
                    "name": values["name"],
                    "description": values["description"],
                    "image_id": values["image_id"]
               }
        return podcasts_in_category

    def get_podcastsInEachRegion(self, region_name):
        """Retrieve all podcast in a region"""
        # Get the id associated with the region_name
        regions = self.get_region()
        for key, values in regions.items():
             if region_name == values["name"]:
                region_id = key
                break
        
        # Use the region id to get the podcast name and description
        podcasts = self.get_podcast_info()
        podcasts_in_region = {}
        for key, values in podcasts.items():
            if values["region_id"] == region_id:
                podcasts_in_region[key] = {
                    "name": values["name"],
                    "description": values["description"],
                    "image_id": values["image_id"]
                }
        return podcasts_in_region
    
    def get_podcastsInEachCountry(self, country_name):
        """Retrieve all podcast in a region"""
        country = self.get_country()
        for key, values in country.items():
            if country_name == values["name"]:
                country_id = key
                break
        if country_id == None:
            print("Country id not found")
            return None
        
        # Use the country id to get the podcast name and description
        podcasts = self.get_podcast_info()
        podcasts_in_country = {}
        for key, values in podcasts.items():
            if values["country_id"] == country_id:
                podcasts_in_country[key] = {
                    "name": values["name"],
                    "description": values["description"],
                    "image_id": values["image_id"]
                }
        return podcasts_in_country

    def get_imageFile_name(self, directory):
        """
        Retrieve the names of image files (ending with .jpg, .jpeg, .png) in the specified directory.

        Args:
        - directory: The path to the directory containing image files.

        Returns:
        - A list containing the names of image files.
        """
        # Initialize an empty list to store file names
        image_file_names = []
        # Check if the directory exists
        if os.path.exists(directory) and os.path.isdir(directory):
            # Iterate over all files in the directory
            for filename in os.listdir(directory):
                # Check if the file ends with .jpg, .jpeg, or .png
                if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                    # Append the file name to the list
                    image_file_names.append(filename)
        else:
            print(f"Directory '{directory}' does not exist or is not a valid directory.")

        return image_file_names
    
    def get_linkFromFile(self, category_info, file_names):
        """get the link"""
        podcast_box = {}
        for key, values in category_info.items():
            for name in file_names:
                try:
                    digit_name = name.split('_')
                    if len(digit_name) > 1:
                        tokenized_num = digit_name[0]
                        if tokenized_num.isdigit():
                            if values["image_id"] == int(tokenized_num):
                                image_path = name
                                podcast_box[image_path] = {
                                    "item_name": values["name"]
                                }
                except Exception as e:
                    print(f"Error processing filename {name}: {e}")
        return podcast_box


    def display_sixpodcast(self, country):
        """display podacst and radio in the landing page"""
        # pod_region_names = self.get_podcastsInEachRegion(region)
        pod_country_names = self.get_podcastsInEachCountry(country)

        if pod_country_names is None:
            print(f"No podcasts found in country '{country}'")
            return {}
        else:
            image_dir = "/home/pc/Yimbo/model_podcast/static/r_pics"
            pic_names = self.get_imageFile_name(image_dir)

            pod_country = self.get_linkFromFile(pod_country_names, pic_names)
            
            Podcast_channel = {}
            count = 1
            for keys, values in pod_country.items():
                if count > 6:
                    break
                else:
                    Podcast_channel[keys] = {
                        "name": values["item_name"]
                    }
                count += 1
            
            return Podcast_channel

        # if pod_country_names is None:
        #    print(f"No podcasts found in region '{region}'")
        #    pod_region = {}
        # else:
        #    image_dir = "/home/pc/Yimbo/model_podcast/static/r_pics"
        #    pic_names = self.get_imageFile_name(image_dir)

        #    pod_region = self.get_linkFromFile(pod_region_names, pic_names)

        # if pod_country_names is None:
        #    print(f"No podcasts found in country '{country}'")
        #    pod_country = {}
        # else:
        #    image_dir = "/home/pc/Yimbo/model_podcast/static/r_pics"
        #    pic_names = self.get_imageFile_name(image_dir)

        #    pod_country = self.get_linkFromFile(pod_country_names, pic_names)

        # create dictionary to store 6 podcast channels
        # podcast_channel = {}
        # count = 1
        # for key, values in pod_region.items():
        #    if count == 4:
        #        break
        #    else:
        #        podcast_channel[count] = {
        #            "image_path": key,
        #            "name": values["item_name"]
        #        }
        #    count += 1

        
