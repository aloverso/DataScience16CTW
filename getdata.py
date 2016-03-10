import urllib2
import urllib
import json
import csv
from bs4 import BeautifulSoup
import numpy as np
from math import radians, sin, cos, asin, sqrt
import pandas
from waitingtime import abbrevs, waitingtime, minabcost
from totaltimes import get_total_times
from amadeus import Hotels
import geopy
from geopy.geocoders import Nominatim

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
	state = ""

	for index, row in data.iterrows():
		latitude = row.latitude
		longitude = row.longitude
		distance = dist(lat,lon,latitude,longitude)
		if distance < d:
			d = distance
			closest = latitude,longitude
			state = row.state
	return closest, state


# formates a latitude and longitude into comma-separated string
# used in making the GMaps API call
def llf(lat, lon):
	return str(lat) + "," + str(lon)

# gets the drive time between two points using their lat/long coordinates
# makes google maps API call
def get_drive_time(lat1, lon1, lat2, lon2, item):
	apikey = "XXXXXXXXXXXXXXXXXXXXX" # put key here
	url = "https://maps.googleapis.com/maps/api/distancematrix/json?" + \
		"origins=" + llf(lat1,lon1) + \
		"&destinations=" + llf(lat2,lon2) + \
		"&key=" + apikey
	result= json.load(urllib.urlopen(url))
	try:
		res = result['rows'][0]['elements'][0][item]['value']
		#print res*00.000621371
		if item == "distance":
			return res*0.000621371 # convert m to miles
		elif item == "duration":
			return res/60 # convert sec to minutes
	except:
		print "==============="
		print lat1, lon1
		print lat2, lon2
		print "==============="
		return np.nan

'''
writes drives.csv
takes each US cities in cities.csv and find the drivetime in minutes (using Google Maps API)
to the closest abortion clinic in ablocs.csv
'''
def get_drivetime_data():

	data = pandas.read_csv('ablocs.csv') 
	cities = pandas.read_csv('cities.csv') 

	f = csv.writer(open("drivedist.csv", "wb+"))

	for index, row in cities.iterrows():
		if index < 14880:
			continue
		lat = row.lat
		lon = row.lng
		#closest, state = get_closest(lat,lon)
		# print lat,lon
		# print closest[0], closest[1]
		drivetime = get_drive_time(lat,lon,row.cliniclat,row.cliniclng, "distance")
		f.writerow([drivetime])
		print lat, lon

def write_totaltime_data():
	# for lat, lng:
	# 	state_abbrev = cities.state[]
	tt_list = []
	hn_list = []
	tdt_list = []
	counter = 0	

	for index, row in cities.iterrows():
		dt = row.drivetime/60
		#geolocator = Nominatim()

		# g = geocoder.google([row.cliniclat, row.cliniclng], method='reverse')
		# state_of_clinic = g.state_long
		#location = geolocator.reverse(str(row.cliniclat)+","+str(row.cliniclng), timeout=10)
		state_of_clinic = row.clinicstate
		# print row.cliniclat, row.cliniclng
		#print state_of_clinic

		wt = waitingtime[abbrevs[state_of_clinic]]
		total_time, hotel_night, total_dt = get_total_times(dt, wt)
		tt_list.append(total_time)
		hn_list.append(hotel_night)
		tdt_list.append(total_dt)
		if hotel_night > 0:
			# print row
			counter += 1
		print index

	print counter
		#print index
	cities['totaltime'] = pandas.Series(tt_list, index=cities.index)
	cities['hotelnights'] = pandas.Series(hn_list, index=cities.index)
	cities['totaldrivetime'] = pandas.Series(tdt_list, index=cities.index)
	cities.to_csv('cities_new.csv')

def write_closest_clinic():
	clinic_lat_list = []
	clinic_lon_list = []
	clinic_state_list = []
	for index, row in cities.iterrows():
		(clinic_lat, clinic_lon), clinic_state = get_closest(row.lat, row.lng)
		clinic_lat_list.append(clinic_lat)
		clinic_lon_list.append(clinic_lon)
		clinic_state_list.append(clinic_state)
		print index
	cities['cliniclat'] = pandas.Series(clinic_lat_list, index=cities.index)
	cities['cliniclng'] = pandas.Series(clinic_lon_list, index=cities.index)	
	cities['clinicstate'] = pandas.Series(clinic_state_list, index=cities.index)	
	cities.to_csv('cities.csv')

def write_hotel_cost():
	hotelcost_minlist = []
	hotelcost_avglist = []
	hotels = Hotels('GQaoTLNPrA1cGxgbAPgWnmvQDicfiwr7')

	for index, row in cities.iterrows():
		if row.hotelnights > 0:
			radius=10
			resp = []
			while len(resp)==0:
				resp = hotels.search_circle(
					check_in='2016-03-10',
					check_out='2016-03-11',
					latitude=row.cliniclat,
					longitude=row.cliniclng,
					currency='USD',
					max_rate=200,
					radius=radius)
				radius+=5

			# ensures that resp has a hotel in it
			mincost = 1000
			totcost = 0
			totnum = 0
			for x in resp['results']:
				cost = float(x['min_daily_rate']['amount'])
				totcost += cost
				totnum +=1
				if cost<mincost:
					mincost=cost
			hotelcost_minlist.append(mincost*row.hotelnights)
			avgcost = float(totcost)/totnum
			hotelcost_avglist.append(avgcost*row.hotelnights)
			print "=====", mincost*row.hotelnights

		else:
			hotelcost_minlist.append(0)
			hotelcost_avglist.append(0)
		print index
	cities['avghotelcost'] = pandas.Series(hotelcost_avglist, index=cities.index)	
	cities['minhotelcost'] = pandas.Series(hotelcost_minlist, index=cities.index)	
	cities.to_csv('cities_new.csv')

def make_statewide_avgs():
	d = {}

	for index,row in cities.iterrows():
		d.setdefault(row.state, {})

		for attr in attrs:
			d[row.state].setdefault(attr, 0)
			d[row.state][attr] += row[attr]
		d[row.state].setdefault("counter", 0)
		d[row.state]["counter"] += 1
		
		print index

	statelist = sorted(d.keys())

	print d

	def get_attr(attr):
		l = []
		for state, sd in sorted(d.iteritems()):
			l.append(float(sd[attr])/sd["counter"])
		print l
		return l

	stateavgs = pandas.DataFrame({
		"state" : statelist,
		"drivetime" : get_attr("drivetime"),
		"totaltime" : get_attr("totaltime"),
		"hotelnights" : get_attr("hotelnights"),
		"totaldrivetime" : get_attr("totaldrivetime"),
		"avghotelcost" : get_attr("avghotelcost"),
		"minhotelcost" : get_attr("minhotelcost"),
		"gasprice" : get_attr("gasprice"),
		"avghrwage" : get_attr("avghrwage"),
		"drivedist" : get_attr("drivedist"),
		"drivetimehrs" : get_attr("drivetimehrs"),
		"numtrips" : get_attr("numtrips"),
		"gascost" : get_attr("gascost"),
		"wageloss" : get_attr("wageloss"),
		"minabcost" : get_attr("minabcost")
		})

	stateavgs.to_csv("stateavgs.csv")

def convert_drivetime_data():
	drivetimes_hours = []
	num_trips = []
	for index, row in cities.iterrows():
		if row.drivetime > 0:
			h = row.drivetime/60.0
			drivetimes_hours.append(h)
			num_trips.append(round(row.totaldrivetime/h))
			print index
		else:
			drivetimes_hours.append(np.nan)
			num_trips.append(np.nan)
	cities['drivetimehrs'] = pandas.Series(drivetimes_hours, index=cities.index)	
	cities['numtrips'] = pandas.Series(num_trips, index=cities.index)
	cities.to_csv('cities_new.csv')

def write_gas_data():
	# gas source
	#http://fuelgaugereport.aaa.com/todays-gas-prices/
	gas = pandas.read_csv('gas.csv')
	gas_price_list = []
	gas_total_cost_list = []
	avg_mpg = 23.4 
	# source http://www.rita.dot.gov/bts/sites/rita.dot.gov.bts/files/publications/national_transportation_statistics/html/table_04_23.html
	
	for index, row in cities.iterrows():
		avgprice = gas.Regular[gas.State == abbrevs[row.state]].iloc[0]
		avgprice = float(avgprice[1:])
		gas_price_list.append(avgprice)
		gas_total_cost_list.append(row.drivedist/avg_mpg*avgprice*row.numtrips)
		print index
	cities['gasprice'] = pandas.Series(gas_price_list, index=cities.index)	
	cities['gascost'] = pandas.Series(gas_total_cost_list, index=cities.index)	
	cities.to_csv('cities_new.csv')

def write_abcost_data():
	abcost_list = []
	for index, row in cities.iterrows():
		abcost_list.append(minabcost[abbrevs[row.state]])
		print index
	cities['minabcost'] = pandas.Series(abcost_list, index=cities.index)	
	cities.to_csv('cities_new.csv')

def write_wageloss_data():
	wageloss_list = []
	for index, row in cities.iterrows():
		wageloss_list.append(row.avghrwage*row.totaltime)
		print index
	cities['wageloss'] = pandas.Series(wageloss_list, index=cities.index)	
	cities.to_csv('cities_new.csv')

def clean_data():
	grouplist = []

	for name, group in cities.groupby("state"):
		for attr in attrs:
			group[attr] = group[attr].fillna(group[attr].median())
		grouplist.append(group)

	frames = pandas.concat(grouplist)
	#print frames.head()

	#print sum(frames["drivetime"].isnull())
	frames.to_csv('cities_clean.csv')

if __name__ == "__main__":
	cities = pandas.read_csv('cities_new.csv')
	data = pandas.read_csv('ablocs.csv')
	# uncomment as needed
	#cities = cities.dropna()
	#print sum(cities["drivetime"].isnull())
	#write_gas_data()
	#write_wageloss_data()
	#write_abcost_data()
	#convert_drivetime_data()
	attrs = ["drivetime","totaltime","hotelnights","totaldrivetime","avghotelcost","minhotelcost","gasprice","avghrwage","drivedist","drivetimehrs","numtrips","gascost","wageloss","minabcost"]
	#clean_data()
	# grouplist = []

	# for name, group in cities.groupby("state"):
	# 	for attr in attrs:
	# 		group[attr] = group[attr].fillna(group[attr].median())
	# 	grouplist.append(group)

	# frames = pandas.concat(grouplist)
	# print frames.head()

	#print sum(cities["totaltime"][cities.state == "WA"])

	#print len(cities[cities.state == "WA"])
	make_statewide_avgs()

	#write_hotel_cost()
	#write_totaltime_data()
	#write_closest_clinic()
	# get_clinic_location_data()
	# get_traplaw_numbers_data()
	#get_drivetime_data()
