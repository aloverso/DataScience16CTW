import urllib2
import urllib
import json
import csv
from bs4 import BeautifulSoup
import numpy as np
from math import radians, sin, cos, asin, sqrt
import pandas
from waitingtime import abbrevs, waitingtime
from totaltimes import get_total_times
'''
writes ablocs.csv
contains each clinic name, location, and latitude/longitude
'''
def get_clinic_location_data():
	url = "http://abortiondocs.org/search-results/?clinic_type=1&ajax=true&query=SResultsMap"
	data = urllib2.urlopen(url).read()
	data = json.loads(data)

	f = csv.writer(open("ablocs2.csv", "wb+"))

	# Write CSV Header
	f.writerow(["name", "city", "state", "zip", "latitude", "longitude"])

	for x in data:
		f.writerow([x["name"],
					x["city"], 
					x["state"], 
					str(x["zip"]), 
					x["latitude"],
					x["longitude"]])

'''
writes ablaws.csv
contains each state and the number of TRAP laws in the state
'''
def get_traplaw_numbers_data():
	site= 'http://data.rhrealitycheck.org/'

	# need this or else you get permission denied error
	hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
		   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
		   'Accept-Encoding': 'none',
		   'Accept-Language': 'en-US,en;q=0.8',
		   'Connection': 'keep-alive'}

	req = urllib2.Request(site, headers=hdr)

	try:
		page = urllib2.urlopen(req)
	except urllib2.HTTPError, e:
		print e.fp.read()

	content = page.read()
	soup = BeautifulSoup(content, "lxml")

	# use beautiful soup to test finding the info we want
	a = soup.find_all("div", class_="state-info")
	print a[0]
	print a[0].h2.get_text()
	print a[0].find_all("tr")[1].td.get_text()

	f = csv.writer(open("ablaws2.csv", "wb+"))

	# Write CSV Header, If you dont need that, remove this line
	f.writerow(["state", "numlaws"])

	for x in a:
		f.writerow([x.h2.get_text(), # the state name
					x.find_all("tr")[1].td.get_text()]) # the number of laws

'''
writes drives.csv
takes each US cities in cities.csv and find the drivetime in minutes (using Google Maps API)
to the closest abortion clinic in ablocs.csv
'''
def get_drivetime_data():

	data = pandas.read_csv('ablocs.csv') 
	cities = pandas.read_csv('cities.csv') 

	f = csv.writer(open("drivetimes.csv", "wb+"))

	# get distance between two points on earth
	# used to determine which abortion clinic is closest to a given city
	def dist(a1, b1, a2, b2):
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

	# given the latitude and longitude of a city (and the ablocs.csv data)
	# returns the lat/long of abortion clinic closest to the city
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

	# formates a latitude and longitude into comma-separated string
	# used in making the GMaps API call
	def llf(lat, lon):
		return str(lat) + "," + str(lon)

	# gets the drive time between two points using their lat/long coordinates
	# makes google maps API call
	def get_drive_time(lat1, lon1, lat2, lon2):
		apikey = "XXXXXXXXXXXXXXXXXXXXXX" # put key here
		url = "https://maps.googleapis.com/maps/api/distancematrix/json?" + \
			"origins=" + llf(lat1,lon1) + \
			"&destinations=" + llf(lat2,lon2) + \
			"&key=" + apikey
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

	# loops through cities lat/longs
	# calculates closest and drivetime
	# writes to csv
	def write_drivetimes():
		for lat in cities.lat:
			lon = cities.lng[cities.lat==lat].iloc[0]
			closest = get_closest(lat,lon)
			# print lat,lon
			# print closest[0], closest[1]
			drivetime = get_drive_time(lat,lon,closest[0],closest[1])
			f.writerow([drivetime/60])
			print lat, lon

	write_drivetimes()

def write_totaltime_data():
	# for lat, lng:
	# 	state_abbrev = cities.state[]
	cities = pandas.read_csv('cities.csv') 
	tt_list = []
	hn_list = []
	tdt_list = []
	counter = 0	
	for index, row in cities.iterrows():
		dt = row.drivetime/60
		wt = waitingtime[abbrevs[row.state]]
		total_time, hotel_night, total_dt = get_total_times(dt, wt)
		tt_list.append(total_time)
		hn_list.append(hotel_night)
		tdt_list.append(total_dt)
		if hotel_night > 0:
			# print row
		 	counter += 1
	print counter
		#print index
	cities['totaltime'] = pandas.Series(tt_list, index=cities.index)
	cities['hotelnights'] = pandas.Series(hn_list, index=cities.index)
	cities['totaldrivetime'] = pandas.Series(tdt_list, index=cities.index)
	cities.to_csv('cities.csv')

if __name__ == "__main__":
	# uncomment as needed
	write_totaltime_data()
	# get_clinic_location_data()
	# get_traplaw_numbers_data()
	# get_drivetime_data()
