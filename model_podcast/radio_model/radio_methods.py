#/usr/bin/python3
""" radioi module to hadle all radio methods"""
from .r_model import Radio
from podcast_model.podcast_model import get_db
from sqlalchemy import inspect
from podcast_model.podcast_methods import PodcastMethods
import os

podcast_cls = PodcastMethods()


class RadioMethods():
    """ The radio module """
    def __init__(self, name=None, description=None, region_id=None,
                 country_id=None, image_id=None
                 ):
        """init method to initialize all the instances"""
        self.name = name
        self.description = description
        self.region_id = region_id
        self.country_id = country_id
        self.image_id = None
        
    
    def create_radio(self):
        """add a new radio channel to the database"""
        with get_db() as db:
            new_radioChannel = radio(name=self.name, description=self.description,
                                     region_id=self.region_id, country_id=self.country_id,
                                     image_id=self.image_id
                                     )
            db.add(new_radioChannel)
            db.commit()

            # set the image id to be qual to the radio id
            new_radioChannel.image_id = new_radio.id
            db.commit()
    
    def get_radioInfo(self):
        """ get all the information in the radio table and store in a dictionary"""
        with get_db() as db:
            radio_data = db.query(Radio).all()
            
            radio_info = {}
            # iterate through the radio and store the info in a dictionary
            for data in radio_data:
                radio_info[data.id] = {
                    "name": data.name,
                    "description": data.description,
                    "region_id": data.region_id,
                    "country_id": data.country_id,
                    "image_id": data.image_id,
                    "audio_id": data.audio_id
                }
        return radio_info

    def get_radioInEachRegion(self, region_name):
        """ Retrieve all radio stations in the region """
        region = podcast_cls.get_region()
        region_id = None
        for key, value in region.items():
            if region_name == value["name"]:
                region_id = key
                break

        # use the region_id to get the radio name and descriptions
        radio_data = self.get_radioInfo()
        radio_in_region = {}
        for key, value in radio_data.items():
            if value["region_id"] == region_id:
                radio_in_region[key] = {
                    "name": value["name"],
                    "description": value["description"],
                    "image_id": value["image_id"],
                    "audio_id": value["audio_id"]
                }
        return radio_in_region
    
    def get_radioInEachCountry(self, country_name):
        """Retrive all the radio channels in the country"""
        country = podcast_cls.get_country()
        country_id = None
        for key, value in country.items():
            if country_name == value["name"]:
                country_id = key
                break

        if country_id == None:
            print("country id not found")
            return None

        # use the country id to get the radio channels in the country
        radio_stations = self.get_radioInfo()
        radio_in_country = {}
        for key, value in radio_stations.items():
            if country_id == value["country_id"]:
                radio_in_country[key] = {
                    "name": value["name"],
                    "description": value["description"],
                    "image_id": value["image_id"],
                    "audio_id": value["audio_id"]
                }
        return radio_in_country


    def display_sixradio(self, country):
        """display six radio channel 3 from country & region"""
        ra_country_names = self.get_radioInEachCountry(country)
        # ra_region_names = self.get_radioInEachRegion(region)
        # print(ra_region_names)
        # print("___________")
        # image_dir = "/home/pc/Yimbo/model_podcast/static/r_pics"
        image_dir = "/home/elpastore/ALX-program/portifolio_project/Yimbo/model_podcast/static/r_pics"
        pic_names = podcast_cls.get_imageFile_name(image_dir)

        # ra_region = podcast_cls.get_linkFromFile(ra_region_names, pic_names)
        ra_country = podcast_cls.get_linkFromFile(ra_country_names, pic_names)

        count = 1

        # all radio and podcast items should be stored 3 each in a dictionary and
        # displayed in groups of six
        
        radio_channel = {}
        # print(ra_region)
        for key, values in ra_country.items():
            if count > 6:
                break
            else:
                radio_channel[key] = {
                    "name": values["item_name"]
                }
            count += 1
        # print(radio_channel)
        # print()

        # count = 1
        # for keys, values in ra_country.items():
        #  if count > 6:
        #        break
        #    else:
        #        radio_channel[count + 3] = {
        #           "image_path": keys,
        #           "name": values["item_name"]
        #        }
        #    count += 1
        
        return radio_channel
