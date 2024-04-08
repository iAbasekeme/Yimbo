#!/usr/bin/python3

from flask import Flask, render_template, request, jsonify
from podcast_model.podcast_methods import PodcastMethods
from radio_model.radio_methods import RadioMethods

app = Flask(__name__)
podcast_method = PodcastMethods()
radio_method = RadioMethods()


te      app.run(host='0.0.0.0', port=5000)
