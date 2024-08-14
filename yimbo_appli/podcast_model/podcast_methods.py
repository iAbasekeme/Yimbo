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

    def process_data(data):
        """
        Process data and extract the ID and cat_id string from the data.
        
        Returns:
            A list containing the extracted ID (as an integer) and cat_id (as a string),
            or None if the data is empty or invalid.
        """
       
        if not data:
            return None
        
        extracted_list = []
        # Find the index of the underscore
        underscore_index = data.find('_')
        
        # If an underscore is found
        if underscore_index != -1:
            # Extract the ID portion (before the underscore)
            id_str = data[:underscore_index]
            
            try:
                extracted_id = int(id_str)
            except ValueError:
                print("Invalid ID: Cannot convert to integer.")
                return None
            
            extracted_list.append(extracted_id)
            
            # Extract the cat_id portion (after the underscore)
            extracted_str = data[underscore_index + 1:]
            
            # Add the cat_id to the list
            extracted_list.append(extracted_str)
        
        # Return the list containing the extracted ID and cat_id
        return extracted_list

    def get_category(self, category_id):
        """
        Retrieve the category name and its associated items.

        args:
            category_id (int): The ID of the category to retrieve.

        Returns:
            dict: A dictionary containing the category and its items.
                The keys are the item IDs and the values are dictionaries
                with a key "name" for each item's name.

        Note:
            get_db() returns a context manager for a database session,
            and Category is a SQLAlchemy model class representing a category in the database.
        """
        # Ensure category_id is an integer
        if not isinstance(category_id, int):
            raise TypeError(f"{category_id} must be of type int")

        category = {}
        try:
           with get_db() as db:
                queried_category = db.query(Category).filter_by(id=category_id).first()
                if not queried_category:
                    raise ValueError("")
                    category[queried_category.id] = {"name": queried_category.name}
          
        except Exception as e:
            # Handle any exception that may occur during the database operation
            print(f"An error occurred: {e}")
            return None

        return category

    def get_podcast(self, data):
        """
        Retrieve podcasts based on the provided data.

        Parameters:
            data (list): A list containing a string value representing 
            the category/region/country identifier.

        Returns:
            dict: A dictionary containing data of the podcasts with the specified ID.
                The keys are the podcast IDs, and the values are dictionaries containing
                various attributes of each podcast, such as name, description, category ID,
                region, country ID, image ID, audio ID, picture, and audio file.

        Raises:
            ValueError: If no podcasts are found for the specified ID.
            TypeError: If `data` is not in the expected format or the data types are invalid.
        """
        if not data or not isinstance(data, list):
            raise TypeError("data should be a list")

        data_list = self.process_data(data)
        if not data_list or not isinstance(data_list, list):
            raise TypeError("Processed data is invalid")

        # Initialize data ID and category/region/country ID variables
        data_id = data_list[0]

        # 'cat_id', 'reg_id', or 'coun_id'
        data_type = data_list[1]

        if not isinstance(data_id, int):
            raise TypeError(f"data_id should be an integer, got {type(data_id)}")

        # Initialize podcasts dictionary
        podcasts = {}

        try:
            # Establish database connection
            with get_db() as db:
                if data_type == "cat_id":
                    queried_podcasts = db.query(Podcast).filter_by(category_id=data_id).all()
                elif data_type == "reg_id":
                    queried_podcasts = db.query(Podcast).filter_by(region_id=data_id).all()
                elif data_type == "coun_id":
                    queried_podcasts = db.query(Podcast).filter_by(country_id=data_id).all()
                else:
                    raise ValueError("Invalid data type")

                if not queried_podcasts:
                    raise ValueError(f"No podcasts found for ID: {data_id} of type {data_type}")

                # Construct dictionary with podcast information
                for podcast in queried_podcasts:
                    podcasts[podcast.id] = {
                        "name": podcast.name,
                        "description": podcast.description,
                        "category_id": podcast.category_id,
                        "region": podcast.region_id,
                        "country_id": podcast.country_id,
                        "image_id": podcast.image_id,
                        "audio_id": podcast.audio_id,
                        "picture": podcast.picture,
                        "audio_file": podcast.audio_file
                    }

        except Exception as e:
            print(f"An error occurred: {e}")
            return None

        return podcasts


    def get_region(self, region_id):
        """
        Retrieve the region name and its associated id.

        args:
            category_id (int): The ID of the region to retrieve.

        Returns:
            dict: A dictionary containing the category and its items.
                The keys are the item IDs and the values are dictionaries
                with a key "name" for each item's name.

        Note:
            get_db() returns a context manager for a database session,
            and Region is a SQLAlchemy model class representing a Region in the database.
        """
        # Ensure category_id is an integer
        if not isinstance(region_id, int):
            raise TypeError(f"{region_id} must be of type int")

        region = {}
        try:
           with get_db() as db:
                queried_category = db.query(Region).filter_by(id=region_id).first()
                if not queried_category:
                    raise ValueError(f"No region found with the region_id: {region_id}")
                
                region[queried_category.id] = {"name": queried_category.name}
          
        except Exception as e:
            # Handle any exception that may occur during the database operation
            print(f"An error occurred: {e}")
            return None

        return region

    def get_country(self, country_id):
        """
        Retrieve the country name and its associated id.

        args:
            country_id (int): The ID of the country to retrieve.

        Returns:
            dict: A dictionary containing the country and its items.
                The keys are the item IDs and the values are dictionaries
                with a key "name" for each item's name.

        Note:
            get_db() returns a context manager for a database session,
            and Country is a SQLAlchemy model class representing a Region in the database.
        """
        # Ensure category_id is an integer
        if not isinstance(country_id, int):
            raise TypeError(f"{country_id} must be of type int")

        country = {}
        try:
           with get_db() as db:
                queried_country = db.query(country).filter_by(id=country_id).first()
                if not queried_country:
                    raise ValueError(f"No country found with the country_id: {country_id}")
                
                country[queried_country.id] = {"name": queried_country.name}
          
        except Exception as e:
            # Handle any exception that may occur during the database operation
            print(f"An error occurred: {e}")
            return None

        return country



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
                    "image_id": podcast.image_id,
                    "audio_id": podcast.audio_id
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
                    "image_id": values["image_id"],
                    "audio_id": values["audio_id"]
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
                    "image_id": values["image_id"],
                    "audio_id": values["audio_id"]
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
                    "image_id": values["image_id"],
                    "audio_id": values["audio_id"]
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
        """Get the link"""
        if not category_info:
            return None
        
        if isinstance(category_info, dict):
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
                                        "item_name": values["name"],
                                        "audio_id": values["audio_id"],
                                        "description": values["description"]
                                    }
                    except Exception as e:
                        print(f"Error processing filename {name}: {e}")
            return podcast_box


    def get_audio_link_from_file(self, audio_id, audio_tracks):
        """get the audio path"""
        if audio_id is not None and audio_tracks is not None:
            if isinstance(audio_id, int):
                image_path = None
                for name in audio_tracks:
                    try:
                        digit_name = name.split('_')
                        if len(digit_name) > 1:
                            tokenized_num = digit_name[0]
                            if tokenized_num.isdigit():
                                if audio_id == int(tokenized_num):
                                    image_path = name
                                    print(image_path)
                    except Exception as e:
                        print(f"Error processing filename {name}: {e}")
                if not image_path:
                    image_path = "Audio content is Unavailable"
                return image_path


    def get_audioFiles(self, directory):
        """
        Retrieve the names of audio files (ending with .mp3) in the specified directory.

        Args:
        - directory: The path to the directory containing image files.

        Returns:
        - A list containing the names of image files.
        """
        # Initialize an empty list to store file names
        audio_file_names = []
        # Check if the directory exists
        if os.path.exists(directory) and os.path.isdir(directory):
            # Iterate over all files in the directory
            for filename in os.listdir(directory):
                # Check if the file ends with .mp3
                if filename.lower().endswith(('.mp3')):
                    # Append the file name to the list
                    audio_file_names.append(filename)
        else:
            print(f"Directory '{directory}' does not exist or is not a valid directory.")

        return audio_file_names

    def display_sixpodcast(self, country):
        """display podacst and radio in the landing page"""
        # pod_region_names = self.get_podcastsInEachRegion(region)
        pod_country_names = self.get_podcastsInEachCountry(country)

        if pod_country_names is None:
            print(f"No podcasts found in country '{country}'")
            return {}
        else:
            # image_dir = "/home/pc/Yimbo/model_podcast/static/r_pics"
            #image_dir = "/home/pc/Yimbo/model_podcast/static/pics"
            image_dir = "/home/elpastore/Yimbo/yimbo_appli/pics"

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
        #    image_dir = "/home/elpastore/Yimbo/yimbo_appli/r_pics"
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

        
