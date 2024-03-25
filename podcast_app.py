#!/usr/bin/python3
""" podcast flask app"""

from flask import Flask, render_template, request, url_for
from podcast_model import Category, Region, Country, Podcast, get_db
from sqlalchemy import inspect

def _repr_(self):
    "this method prits the str format of the podcast name and id"""
    return f"podcast(id={self.id}, name="{self.name}")"

def get_tableName():
        """retrieve the names of all the tables in tha database"""
        with get_db() as db:
             table_name = inspect(url_for)
             name_tab = []
             for name in table_name.get_table_name():
                  name_tab[name] = name
        return name_tab

def category_name():
     """retrieve the category name"""
     with get_db() as db:
        category_name = db().query(Category).filter_by(name=name).all()
        return category_name

def region_name():
     """retrieve the region name"""
     with get_db() as db:
        region_name_name = db().query(Region).filter_by(region=name).all()
        return region_name

def country_name():
     """retrieve the country name"""
     with get_db() as db:
        country_name_name = db().query(Category).filter_by(name=name).all()
        if country_name:
            return category_name
        else:
            raise 404 erro

@app_route("/")
def podcast():
    category_name = category_name()
    table_name = get_tableName()
    country_name = country_name()
    region_name = region_name()

    return render_template("podcast_page.html",  category_name=category_name,
                           table_name=table_name, country_name=country_name,
                           region_name=region_name)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
