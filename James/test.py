
import pandas as pd 
import numpy as np
import geocoder


# # address = "Columbia town, AL"
# address = 'Florida'
# g = geocoder.google(address)
# print g.latlng


name = "Florida"
from geopy.geocoders import Nominatim
geolocator = Nominatim()
location = geolocator.geocode(name)
print location.longitude
print location.latitude


# # import geocoder
# # g = geocoder.google('Mountain View, CA')
# # print g.latlng
# # (37.3860517, -122.0838511)


# from geopy.geocoders import Nominatim
# geolocator = Nominatim()
# location = geolocator.geocode("Alabama")
# # >>> print(location.address)
# # Flatiron Building, 175, 5th Avenue, Flatiron, New York, NYC, New York, ...
# print((location.latitude, location.longitude))
# # (40.7410861, -73.9896297241625)



# df = pd.read_csv('StateAreaList.csv')

# print df.columns  
# print df.iloc[:, 0]
# print df.State
# print df.at[0,'State']
# print df.loc['State']
# print df[df.State == "u'Alaska'"].Area
