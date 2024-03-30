#!/usr/bin/python3

from flask import Flask, render_template, request, jsonify
from podcast_methods import PodcastMethods

app = Flask(__name__)
podcast_method = PodcastMethods()


@app.route("/sort_category", methods=["GET", "POST"], strict_slashes=False)
def sort_category():
    """ retrieve the category name and get all podcasts belonging
        to that group
    """ 

    # retrive the request
    group_names = request.args.get("category")
    table_names = request.args.get("table_names")
    category_info = podcast_method.get_podcastsInEachCategory(group_names)
    pic_names = podcast_method.get_imageFile_name("/home/pc/Yimbo/model_podcast/static/pics")
    podcast_info =  podcast_method.get_linkFromFile(category_info, pic_names)
    
    # Render the template and pass the category and table names as context variables
    return render_template("new.html", group_names=group_names,
                           podcast_info=podcast_info)


@app.route("/sort_region", methods=["GET", "POST"], strict_slashes=False)
def sort_region():
    """ retrieve the region name and get all podcasts belonging
        to that group
    """
    group_names = request.args.get("region")
    table_names = request.args.get("table_names")
    category_info = podcast_method.get_podcastsInEachRegion(group_names)
    image_dir = "/home/pc/Yimbo/model_podcast/static/pics"
    pic_names = podcast_method.get_imageFile_name(image_dir)
    podcast_info =  podcast_method.get_linkFromFile(category_info, pic_names)

    return render_template("new.html",
                           group_names=group_names,
                           podcast_info=podcast_info)


@app.route("/sort_country", methods=["GET", "POST"], strict_slashes=False)
def sort_country():
    """ retrieve the country name and get all podcasts belonging
        to that group
    """

    # retrive the request
    group_names = request.args.get("country")
    table_names = request.args.get("table_names")
    category_info = podcast_method.get_podcastsInEachCountry(group_names)
    image_dir = "/home/pc/Yimbo/model_podcast/static/pics"
    pic_names = podcast_method.get_imageFile_name(image_dir)
    podcast_info =  podcast_method.get_linkFromFile(category_info, pic_names)

    # Render the template and pass the category and table names as context variables
    return render_template("new.html",
                           group_names=group_names,
                           podcast_info=podcast_info,
                           )


@app.route("/", methods=["GET", "POST"], strict_slashes=False)
def podcast():
    category_names = podcast_method.category_names()
    table_names = podcast_method.get_table_name()
    country_names = podcast_method.country_names()
    region_names = podcast_method.region_names()

    return render_template("podcast_page.html",  
                           category_names=category_names,
                           table_names=table_names,
                           country_names=country_names,
                           region_names=region_names)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
