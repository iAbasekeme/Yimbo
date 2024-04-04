from dotenv import load_dotenv
import os
load_dotenv()
import base64
import requests
import json

client_id = os.getenv("CLIENT_ID")
client_secrey = os.getenv("CLIENT_SECRET")


def get_token():
    """
    get the token to be used for authentication
    """
    auth_string = client_id + ':' + client_secrey
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')
    
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,  
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials"
    }
    response = requests.post(url, headers=headers, data=data)  # , verify=False)
    token_info = json.loads(response.content)
    return token_info["access_token"]


def get_auth_header(token):
    """
    return the authorization header
    """
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    """
    GET request to search for an artist
    """
    url ="https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    """parameter = {
        "q": artist_name,
        "type": "artist&limit=1"
    }"""
    query = f"?q={artist_name}&type=artist&limit=1"
    query_url = url + query
    res = requests.get(query_url, headers=headers)
    json_result = json.loads(res.content)["artists"]["items"]
    #json_result = res.json()["artists"]["items"][0].get("id")
    if len(json_result) == 0:
        print("No artist found")
        return None

    return json_result[0]
def get_categories():
    """
    make a GET request to get the categories of music
    """
    token = get_token()
    url = "https://api.spotify.com/v1/browse/categories"
    headers = get_auth_header(token)
    response = requests.get(url, headers=headers)
    json_result = json.loads(response.content)["categories"]["items"]
    return json_result

def get_category_playlists(token, category_id):
    """
    make a GET request to get the playlists in a category
    """
    url = f"https://api.spotify.com/v1/browse/categories/{category_id}/playlists"
    headers = get_auth_header(token)
    response = requests.get(url, headers=headers)
    json_result = json.loads(response.content)["playlists"]["items"]
    return json_result

def get_songs_by_artist(token, artist_id):
    """
    make a GET request to get the top tracks of an artist
    """
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    
    response = requests.get(url, headers=headers)
    json_result = json.loads(response.content)["tracks"]
    return json_result


def get_song_in_playlist(token, playlist_id):
    """
    make a GET request to get the songs in a playlist
    """
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = get_auth_header(token)
    response = requests.get(url, headers=headers)
    #json_result = json.loads(response.content)["items"]
    json_result = response.json()["items"]
    return json_result

def convert_ms_to_min_sec(milliseconds):
    """
    use to convert en milliseconds to minutes and seconds
    """
    seconds = milliseconds / 1000
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes}:{seconds:02d}"

def get_music():
    """
    make a GET request to fetch some african songs using the id of the playlist with the name 'African Music'
    :return: list of song objects from the playlist
    """
    token = get_token()
    songs = get_song_in_playlist(token, "37i9dQZF1DWYkaDif7Ztbp")
    all_songs =[]
    my_songs = {}
    for song in songs:
        #all_songs.append(song.get('track').get('name'))
        my_songs = {
            'name': song.get('track').get('name'),
            'duration': convert_ms_to_min_sec(song.get('track').get('duration_ms')),
            'popularity': song.get('track').get('popularity'),
            'uri': song.get('track').get('uri'),
            'track_id': song.get('track').get('id'),
            'album': song.get('track').get('album').get('name'),
            'release date': song.get('track').get('album').get('release_date'),
            'artist': song.get('track').get('artists')[0].get('name'),
            'picture': song.get('track').get('album').get('images')[0].get('url'),
            'url': song.get('track').get('external_urls').get('spotify')
        }
        all_songs.append(my_songs)
    return all_songs

print(get_category_playlists(get_token(), '0JQ5DAqbMKFNQ0fGp4byGU')[0])