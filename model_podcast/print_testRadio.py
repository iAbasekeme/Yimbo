#!/usr/bin/python3

from radio_model.radio_methods import RadioMethods
from podcast_model.podcast_methods import PodcastMethods

p_cls = PodcastMethods()
r_cls = RadioMethods()

radio_info = r_cls.get_radioInfo()


print("Radio INfo:", radio_info)
print()

region = "South Africa"
radio_in_region = r_cls.get_radioInEachRegion(region)
print("Radio cahnnells in {}: {}".format(region, radio_in_region))
print()

country = "Nigeria"
radio_in_country = r_cls.get_radioInEachCountry(country)
print("radio channels in {}: {}".format(country, radio_in_country))

print()
country = "Senegal"
radio_in_country = r_cls.display_sixradio(country)
print("Six radio channels in {}: {}".format(country, radio_in_country))

print()
country = "Kenya"
podcast_in_country = p_cls.display_sixpodcast(country)
print("Six podcast channels in {}: {}".format(country, podcast_in_country))

print()
_dir = "/home/pc/Yimbo/model_podcast/static/r_music"
file_list = p_cls.get_imageFile_name(_dir)
file_info = p_cls.get_audio_link_from_file(3, file_list)
print(file_info)
print()

audio_id = 6
audio_dir = "/home/pc/Yimbo/model_podcast/static/r_music"
audio_files = p_cls.get_audioFiles(audio_dir)
fileName = p_cls.get_linkFromFile(audio_id, audio_files)
print(fileName)
print()

audio_path = audio_dir + fileName
print(audio_path)