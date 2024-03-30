#!/usr/bin/python3
"""Print the str of all podcast_methods"""

from podcast_methods import PodcastMethods

if __name__ == "__main__":
    # Create an instance of PodcastMethods
    podcast_methods = PodcastMethods()
    
    # Retrieve podcasts in each category
    category_name = "Tech & Science"
    category_info = podcast_methods.get_podcastsInEachCategory(category_name)
    print("podcast in each News & politics:", category_info)
    
    # Retrieve image file names
    image_dir = "/home/pc/Yimbo/model_podcast/static/pics"
    list_image_names = podcast_methods.get_imageFile_name(image_dir)
    print("Names of images in /stactic/pic/ :", list_image_names)
    
    print()
    # Retrieve podcast information from image files
    podcast_info = podcast_methods.get_linkFromFile(category_info, list_image_names, image_dir)
    for key, value in podcast_info.items():
        print("image path: {}, image name: {}".format(key, value["podcast_name"]))
        print()
