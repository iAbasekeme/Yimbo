import requests
import sys
import os
from flask import jsonify
from dotenv import load_dotenv

MY_API_KEY = "8b45ee61f43e5fe313a0b788fe98c2f5"

ACCEPTED_CODES = (
    "DZ", "AO", "BJ", "BW", "BF", "BI", "CM", "CV", "CF", "TD", "KM", "CD", "CJ",
    "EG", "GQ", "ER", "ET", "GA", "GM", "GH", "GN", "GW", "CI", "KE", "LS", "LR",
    "LY", "MG", "MW", "ML", "MR", "MU", "YT", "MA", "MZ", "NA", "NE", "MG", "CG",
    "RE", "RW", "SH", "ST", "SN", "SC", "SL", "SO", "ZA", "SS", "SD", "SZ", "TZ",
    "TG", "TN", "UG", "EH", "ZM", "ZW"
)


def get_artist():
    key = MY_API_KEY
    if key is None:
        print("Error: API key not found in environment variables.")
    api_endpoint = f"https://api.musixmatch.com/ws/1.1/artist.get?artist_id={sys.argv[1]}&apikey={key}"
    headers = {"Authorization": f"Bearer {MY_API_KEY}"}
    response = requests.get(api_endpoint, headers=headers)
    print(response.status_code)
    if response.status_code == 200:
        track_info = response.json()
        try:
            # artist_country = track_info['message']['body']['artist_country']
            artist_country = track_info.get('message', {}).get(
                'body', {}).get('artist', {}).get('artist_country')
            if not artist_country or artist_country not in ACCEPTED_CODES:
                print("Can't get that artist or artist not in africa")
            else:
                print(track_info)
        except (KeyError, AttributeError):
            print(
                "Error retrieving artist information or country data. Check API respons structure.")

get_track()