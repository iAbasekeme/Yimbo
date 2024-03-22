#!/usr/bin/python3
""" podcast flask app"""

from flask import Flask, render_template, request, url_for
from podcast_model import Category, Region, Country, Podcast, get_db


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
