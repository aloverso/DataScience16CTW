import pandas as pd 
import numpy as np
import StateAreaList as const
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim
geolocator = Nominatim()
# import geocoder

# print const.StateAreaList['Alaska']

df = pd.read_csv('../SUB-EST2014_ALL.csv')


# #remove the state entries
stateData = df[df.STNAME == df.NAME]


grouped = df.groupby('STNAME')

lngList =[]
latList =[]
averageAreaList = []

for name, group in grouped:

	try:
		location = geolocator.geocode(name)
		lngList.append(location.longitude)
		latList.append(location.latitude)
		popSum = stateData[stateData.STNAME == name].POPESTIMATE2014
		area = const.StateAreaList[name]
		averageArea = popSum/area	
		averageAreaList.append(averageArea)
	except:
		print "exception"
		print name

	# if name == "District of Columbia":
	# 	print "District of Columbia"
	# 	print "stateData[stateData.STNAME == name].POPESTIMATE2014"
	# 	print stateData[stateData.STNAME == name].POPESTIMATE2014



x = latList
y = averageAreaList
print len(x)
print len(y)
tmp_x = []
tmp_y = []
for i in range(len(x)):
	if x[i] > 30 and x[i] < 50 and y[i] > 100:
		tmp_x.append(float(x[i]))
		tmp_y.append(y[i])
print len(tmp_x)
print len(tmp_y)

MIN = min(tmp_x)
print "min", MIN

print tmp_x
print "------------------------------"
print tmp_y


plt.scatter(tmp_x, tmp_y, alpha=0.5)
plt.show()