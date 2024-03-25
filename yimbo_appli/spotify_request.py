import requests
import json

""" url = "https://spotify-scraper.p.rapidapi.com/v1/genre/contents"

querystring = {"genreId":"0JQ5DAqbMKFNQ0fGp4byGU"}

headers = {
	"X-RapidAPI-Key": "ed409927fbmshac747d2cc471246p199491jsn4eb168a0cb9b",
	"X-RapidAPI-Host": "spotify-scraper.p.rapidapi.com"
}

my_info= {}
response = requests.get(url, headers=headers, params=querystring)
data = response.json()
info = data.get('contents').get('items')[1].get('contents').get('items')[0]

my_info['id'] = info.get('id')
my_info['name'] = info.get('name')

print(f"the name of the playlist is {my_info['name']} and the id is {my_info['id']}")
print(my_info) 



url_2 = "https://spotify-scraper.p.rapidapi.com/v1/playlist/contents"

querystring_2 = {"playlistId":"37i9dQZF1DWYkaDif7Ztbp"}

headers_2 = {
	"X-RapidAPI-Key": "ed409927fbmshac747d2cc471246p199491jsn4eb168a0cb9b",
	"X-RapidAPI-Host": "spotify-scraper.p.rapidapi.com"
}

response_2 = requests.get(url_2, headers=headers_2, params=querystring_2)
music_list = []
music_info = {}
music_data = response_2.json()
if 'contents' in music_data:
    info_2 = music_data.get('contents')
    # music = info_2.get('items')[0]
    for music in info_2.get('items')[0:5]:
        music_info = {
			"type": music.get('type'),
			'name': music.get('name'),
			'durationText': music.get('durationText'),
			'artist_name': music.get('artists')[0].get('name'),
			'artist_id': music.get('artists')[0].get('id'),
			'music_url': music.get('shareUrl')}
        music_list.append(music_info)

print(music_list)"""



url = "https://spotify-scraper.p.rapidapi.com/v1/artist/overview"

querystring = {"artistId":"3SozjO3Lat463tQICI9LcE"}

headers = {
	"X-RapidAPI-Key": "ed409927fbmshac747d2cc471246p199491jsn4eb168a0cb9b",
	"X-RapidAPI-Host": "spotify-scraper.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

if response.status_code == 200:
    data = response.json()
    artist_info = {}
    artist_info['name'] = data.get('name')
    artist_info['id'] = data.get('id')
    artist_info['picture'] = data.get('visuals').get('avatar')[0].get('url')
    
print(artist_info.get('picture'))