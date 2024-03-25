#!/usr/bin/python3
""" podcast flask app"""

from flask import Flask, render_template, request, url_for
from model import Category, Region, Country, Podcast
from podcast_model import get_db
from sqlalchemy import inspect

app = Flask(__name__)

def category_name():
    """retrieve the category name"""
    with get_db() as db:
        # query the db and get all the values from the name column
        category_names = db.query(Category.name).all()
        return category_names

def region_name():
    """retrieve the region name"""
    with get_db() as db:
        # query the region table and get all the values of the name column
        region_names = db.query(Region.name).all()
        return region_names

def country_name():
    """retrieve the country name"""
    with get_db() as db:
        country_names = db.query(Country.name).all()
        if not country_names:
            return None  # Or raise a specific exception like NotFound
        else:
            return country_names
 
def get_table_name():
    """retrieve the table name of the database"""
    with get_db() as db:
        table_names = inspect(db.get_bind()).get_table_names()
    return table_names

@app.route("/", methods=["GET", "POST"], strict_slashes=False)
def podcast():
    category_names = category_name()

    table_names = get_table_name()
    country_names = country_name()
    region_names = region_name()

    return render_template("podcast_page.html",  category_name=category_names,
                           table_name=table_names, country_name=country_names,
                           region_name=region_names)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
