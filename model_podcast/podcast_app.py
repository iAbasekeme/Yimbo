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
    category = request.args.get("category")
    table_names = request.args.get("table_names")
    category_name = podcast_method.get_podcastsInEachCategory(category_name)
   
    
    # Render the template and pass the category and table names as context variables
    return render_template("new.html", category_name=category_name, table_names=table_names)


@app.route("/sort_region", methods=["GET", "POST"], strict_slashes=False)
def sort_region():
    """ retrieve the region name and get all podcasts belonging
        to that group
    """
    region_name = request.args.get("region")
    table_names = request.args.get("table_names")
    category_name = podcast_method.get_podcastsInEachRegion(region_name)
    return render_template("new.html", category_name=category_name, table_names=table_names)


@app.route("/sort_country", methods=["GET", "POST"], strict_slashes=False)
def sort_country():
    """ retrieve the country name and get all podcasts belonging
        to that group
    """

    # retrive the request
    country_name = request.args.get("country")
    table_names = request.args.get("table_names")
    category_name = get_podcastsInEachCountry(country_name)

    # Render the template and pass the category and table names as context variables
    return render_template("new.html", category_name=category_name, table_names=table_names)


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

