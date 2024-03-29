#!/usr/bin/python3
"""Print the str of all podcast_methods"""

import requests

if __name__ == "__main__":
    # Define the JSON data to send in the request
    json_data = {"category": "example_category", "table": "example_table"}

    # Send a POST request to the /sort_bycategory endpoint with JSON data
    response = requests.post("http://localhost:5000/sort_bycategory", json=json_data)

    # Print the response from the server
    print("Response:", response.text)

