#!/usr/bin/python3
"""Print the str of all podcast_methods"""

from podcast_methods import PodcastMethods
from flask import json

if __name__ == "__main__":
    # Create an instance of PodcastMethods
    podcast_methods = PodcastMethods()
    
    
    # Retrieve and print category names
    print("Category Names:", podcast_methods.category_names())
    print()
    # Retrieve and print country names
    print("Country Names:", podcast_methods.country_names())
    print()
    # Retrieve and print region names
    print("Region Names:", podcast_methods.region_names())
    print()
    # Retrieve and print table names
    print("Table Names:", podcast_methods.get_table_name())
    print()
    # Retrieve and print podcast information
    print("Podcast Info:", podcast_methods.get_podcast_info())
    
    print()
    # Retrieve podcasts in each category
    category_name = "News & Politics"
    print("podcast in each News & politics:", podcast_methods.get_podcastsInEachCategory(category_name))
    
    print()
    region_name = "Ethiopia"
    print("podcast in each Ethiopia:", podcast_methods.get_podcastsInEachCountry(region_name))
    
    print()
    country_name = "East Africa"
    print("podcasts in East Africa:", podcast_methods.get_podcastsInEachRegion(country_name))

