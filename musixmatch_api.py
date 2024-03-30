import requests
import sys
from flask import jsonify

MY_API_KEY = "8b45ee61f43e5fe313a0b788fe98c2f5"


def get_track():
    key = MY_API_KEY
    if key is None:
        print("Error: API key not found in environment variables.")

    api_endpoint = f"https://api.musixmatch.com/ws/1.1/artist.get?artist_id={sys.argv[1]}&apikey={key}"
    headers = {"Authorization": f"Bearer {MY_API_KEY}"}
    response = requests.get(api_endpoint, headers=headers)
    print(response.status_code)
    if response.status_code == 200:
        artist_info = response.json()
        # Process artist information
        print(artist_info)
    else:
        print(f"Error: {response.status_code}")
        return None


get_track()
