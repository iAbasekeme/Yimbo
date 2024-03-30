import requests
import sys
import os
from flask import jsonify
from dotenv import load_dotenv

MY_API_KEY = "8b45ee61f43e5fe313a0b788fe98c2f5"


def get_track():
    key = MY_API_KEY
    if key is None:
        print("Error: API key not found in environment variables.")
    api_endpoint = f"https://api.musixmatch.com/ws/1.1/track.get?commontrack_id={sys.argv[1]}&apikey={key}"
    headers = {"Authorization": f"Bearer {MY_API_KEY}"}
    response = requests.get(api_endpoint, headers=headers)
    track_info = response.json()
    print(track_info)


get_track()
