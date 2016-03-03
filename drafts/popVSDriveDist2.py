
import pandas as pd 
import numpy as np
import geocoder

df = pd.read_csv('SUB-EST2014_ALL.csv')

df = df.head(100)


# #remove the state entries
citiesData = df[df.STNAME != df.NAME]
citiesData['lat'] = 0
citiesData['lng'] = 0


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
	g = geocoder.google(address)

	if(len(g.latlng) < 1):
		citiesData.loc[index, 'lat'] = None
	else:
		citiesData.loc[index, 'lat'] = g.latlng[0]


	if(len(g.latlng) < 2):
		citiesData.loc[index, 'lng'] = None		
	else:
		citiesData.loc[index, 'lng'] = g.latlng[1]		

	counter +=1
	if counter%100 == 0:
		print counter
	if counter == length:
		break

	

# latList = np.array(latList)
# lngList = np.array(lngList)	

# latList = pd.DataFrame(latList, columns = ['lat'])
# lngList = pd.DataFrame(latList, columns = ['lng'])


# citiesData['lat'] = latList[['lat']].values.tolist()
# citiesData['lng'] = lngList[['lng']].values.tolist()

# print df.head(3)

citiesData.to_csv('test1.csv')


# def addLatAndLng(passenger_id):
#     age = train.loc[passenger_id, 'Age']
#     if (age < 18):
#         # Add a column while were at it
#         train.loc[passenger_id, 'Child'] = 1
#         return 'child'
#     else:
#         # Add a column while were at it
#         train.loc[passenger_id, 'Child'] = 0
#         return 'adult'

# grouped = train.groupby(child_adult_grouper)
# print grouped["Survived"].mean()