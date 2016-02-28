import pandas
import csv
import json, urllib
import numpy as np

data = pandas.read_csv('ablocs.csv') 

cities = pandas.read_csv('cities.csv') 

from math import radians, sin, cos, asin, sqrt

f = csv.writer(open("drives.csv", "wb+"))

def dist(a1, b1, a2, b2):
    """Gives the distance between two points on earth.
    """
    point1 = (a1,b1)
    point2 = (a2,b2)
    earth_radius_miles = 3956
    lat1, lon1 = (radians(coord) for coord in point1)
    lat2, lon2 = (radians(coord) for coord in point2)
    dlat, dlon = (lat2 - lat1, lon2 - lon1)
    a = sin(dlat/2.0)**2 + cos(lat1) * cos(lat2) * sin(dlon/2.0)**2
    great_circle_distance = 2 * asin(min(1,sqrt(a)))
    d = earth_radius_miles * great_circle_distance
    return d
def get_closest(lat, lon):
	d = 1000000
	closest = 0,0
	for latitude in data.latitude:
		longitude = data.longitude[data.latitude==latitude].iloc[0]
		distance = dist(lat,lon,latitude,longitude)
		if distance < d:
			d = distance
			closest = latitude,longitude
	return closest

def llf(lat, lon):
	return str(lat) + "," + str(lon)

def get_drive_time(lat1, lon1, lat2, lon2):
	apikey = "AIzaSyBhFXT0JtwxspEQFsjI0Uwno5e36VUNTD0"
	url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&key={2}".format(llf(lat1,lon1),llf(lat2,lon2),apikey)
	result= json.load(urllib.urlopen(url))
	try:
		driving_time = result['rows'][0]['elements'][0]['duration']['value']
		return driving_time
	except:
		print "==============="
		print lat1, lon1
		print lat2, lon2
		print "==============="
		return np.nan

def find_close(lat):
	lon = cities.lng[cities.lat==lat].iloc[0]
	closest = get_closest(lat,lon)
	# print lat,lon
	# print closest[0], closest[1]
	drivetime = get_drive_time(lat,lon,closest[0],closest[1])
	f.writerow([drivetime/60])
	print lat, lon
	return drivetime/60

cities['distclosest'] = cities["lat"].apply(lambda l: find_close(l))