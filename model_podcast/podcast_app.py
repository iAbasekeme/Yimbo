#!/usr/bin/python3
""" podcast flask app"""

from flask import Flask, render_template, request, url_for
from podcast_model import Category, Region, Country, Podcast, get_db

app = Flask(__name__)

@app.route("/")
def index():
    """Render the main page with the navigation and dropdown bars"""
    return render_template("yimbo.html")

@app.route("/podcasts/")
@app.route("/podcasts/<string:option>")
def podcasts(option=None):
    """Handles podcast selections (by category, region, or country)"""
    with get_db() as db:
        if option == "General":
            all_podcast = db().query(Podcast).all()
            return render_template("general.html", podcasts=all_podcast)
        elif option == "Category":
            categories = db().query(Category).all()
            return render_template("category.html", categories=categories)
        elif option == "Country":
            countries = db().query(Country).all()
            return render_template("country.html", countries=countries)
        elif option == "Region":
            regions = db().query(Region).all()
            return render_template("region.html", regions=regions)
        else:
            return render_template("error.html", message="Invalid selection")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
