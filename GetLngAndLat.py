import pandas as pd 
import numpy as np
from geopy.geocoders import Nominatim
geolocator = Nominatim()

df = pd.read_csv('SUB-EST2014_ALL.csv')

# df = df.head(10)


# #remove the state entries
citiesData = df[df.STNAME != df.NAME]


length = len(citiesData)

print length

latList = []
lngList = []

counter = 0
for index, row in citiesData.iterrows():
	cityName = row['NAME']
	stateName = row['STNAME']
	address = ",".join((cityName, stateName))
	# print address
	location = geolocator.geocode(address)

	# g = geocoder.google(address)
	# if(len(g.latlng) < 1):
	# 	latList.append(None)
	# else:

		# try:
		# except e:
		# 	print len(g.latlng)

	# if(len(g.latlng) < 2):
	# 	lngList.append(None)
	# else:

	# print address
	# print location
	
	try:
		lngList.append(location.longitude)
		latList.append(location.latitude)
	except Exception as e:
		# print e
		lngList.append(None)
		latList.append(None)


	counter +=1
	if counter%100 == 0:
		print counter
	# if counter == length:
	# 	break

	

latList = np.array(latList)
lngList = np.array(lngList)	
print "latList", latList
print "lngList", lngList


citiesData['lat'] = pd.Series(latList, index=citiesData.index)
citiesData['lng'] = pd.Series(lngList, index=citiesData.index)

# latList = pd.DataFrame(latList, columns = ['lat'])
# lngList = pd.DataFrame(latList, columns = ['lng'])


# citiesData['lat'] = latList
# citiesData['lng'] = lngList

# print df.head(3)

citiesData.to_csv('test2.csv')
