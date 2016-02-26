import matplotlib.cbook as cbook
import matplotlib.pyplot as plt
import pandas

data = pandas.read_csv('ablocs.csv') 


# import numpy as np
from mpl_toolkits.basemap import Basemap
# import matplotlib.pyplot as plt
# import urllib, os

# lats = np.asarray(data.latitude)
# lons = np.asarray(data.longitude)

# #m = Basemap(projection='hammer',lon_0=-90)
# m = Basemap(llcrnrlon=-145.5,llcrnrlat=1.,urcrnrlon=-2.566,urcrnrlat=46.352,\
#             rsphere=(6378137.00,6356752.3142),\
#             resolution='l',area_thresh=1000.,projection='lcc',\
#             lat_1=50.,lon_0=-107.)
# x, y = m(lons,lats)
# m.drawmapboundary(fill_color='#99ffff')
# m.fillcontinents(color='#cc9966',lake_color='#99ffff')
# m.scatter(x,y,30,marker='o',color='k')

# plt.show()

# Create a figure of size (i.e. pretty big)
fig = plt.figure(figsize=(20,10))

# m = Basemap(projection='gall',
#               # with low resolution,
#               resolution = 'l',
#               # And threshold 100000
#               area_thresh = 100000.0,
#               # Centered at 0,0 (i.e null island)
#               lat_0=0, lon_0=0)

m = Basemap(llcrnrlon=-145.5,llcrnrlat=1.,urcrnrlon=-2.566,urcrnrlat=46.352,\
            rsphere=(6378137.00,6356752.3142),\
            resolution='l',area_thresh=1000.,projection='lcc',\
            lat_1=50.,lon_0=-107.)

# # Draw the coastlines on the map
m.drawcoastlines()

# # Draw country borders on the map
m.drawcountries()

# Fill the land with grey
m.fillcontinents(color = '#888888')

# Draw the map boundaries
m.drawmapboundary(fill_color='#f4f4f4')

# Define our longitude and latitude points
# We have to use .values because of a wierd bug when passing pandas data
# to basemap.
x,y = m(data['longitude'].values, data['latitude'].values)

# Plot them using round markers of size 6
m.plot(x, y, 'ro', markersize=6)

# Show the map
plt.show()