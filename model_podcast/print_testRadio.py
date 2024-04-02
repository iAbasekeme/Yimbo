#!/usr/bin/python3

from radio_model.radio_methods import RadioMethods

r_cls = RadioMethods()
radio_info = r_cls.get_radioInfo()
print("Radio INfo:", radio_info)
print()

region = "North Africa"
radio_in_region = r_cls.get_radioInEachRegion(region)
print("Radio cahnnells in {}: {}".format(region, radio_in_region))
print()

country = "South Africa"
radio_in_country = r_cls.get_radioInEachCountry(country)
print("radio channels in {}: {}".format(country, radio_in_country))
