import matplotlib.cbook as cbook
import matplotlib.pyplot as plt
import pandas
from mpl_toolkits.basemap import Basemap
import numpy as np
from matplotlib.colors import rgb2hex
from matplotlib.patches import Polygon

data = pandas.read_csv('ablocs.csv') 
cities = pandas.read_csv('cities.csv')
lawsdata = pandas.read_csv('ablaws.csv')

def plot_clinic_locations():
	fig = plt.figure(figsize=(20,10))

	# define the map
	m = Basemap(llcrnrlon=-145.5,llcrnrlat=1.,urcrnrlon=-2.566,urcrnrlat=46.352,\
				rsphere=(6378137.00,6356752.3142),\
				resolution='l',area_thresh=1000.,projection='lcc',\
				lat_1=50.,lon_0=-107.)

	# # Draw the coastlines on the map
	m.drawcoastlines()

	# # Draw country borders on the map
	m.drawcountries()

	# Fill the land with grey
	m.fillcontinents(color = '#888888', zorder=0)

	# Draw the map boundaries
	m.drawmapboundary(fill_color='#f4f4f4')

	# Define our longitude and latitude points
	# We have to use .values because of a wierd bug when passing pandas data
	# to basemap.
	x,y = m(cities['lng'].values, cities['lat'].values)

	# Plot them using round red markers of size 6
	for lat in data.latitude:
		lon = data.longitude[data.latitude==lat].iloc[0]
		x,y = m(lon, lat)
		m.plot(x, y, marker='o', color='r', markersize=6)

	# Show the map
	plt.show()

def get_maps():
	map_lower_48 = Basemap(llcrnrlon=-119,llcrnrlat=22,urcrnrlon=-64,urcrnrlat=49,  
				projection='lcc',lat_1=33,lat_2=45,lon_0=-95)

	states_shp_info = map_lower_48.readshapefile('shapefiles/st99_d00', 'states',drawbounds=True)

	m_alaska = Basemap(llcrnrlon=-173,llcrnrlat=51,urcrnrlon=-134.45,urcrnrlat=71.34,
					   projection='lcc', lat_0=64, lon_0=-151)

	alaska_shp_info = m_alaska.readshapefile('shapefiles/st99_d00', 'states',drawbounds=True)


	m_hawaii = Basemap(#llcrnrlon=-161,llcrnrlat=21,urcrnrlon=-154,urcrnrlat=22,
					   width=800000, height=500000,
					   projection='lcc', 
					   lat_0=20.525, lon_0=-157.385,
					   lon_1=-158.115, lat_1=17.24,
					   lon_2=-153.479, lat_2=19.663, 
					   )

	hawaii_shp_info = m_hawaii.readshapefile('shapefiles/st99_d00', 'states',drawbounds=True)

	return map_lower_48, m_alaska, m_hawaii

# make a colormap coloring each state according to its value in dictionary d
def make_statemap(d):
	map_lower_48, m_alaska, m_hawaii = get_maps()

	cmap = plt.cm.Blues
	vmin = 0; vmax = 1

	fig = plt.figure(figsize = (15, 24), dpi=300)

	ax_mainland = plt.subplot2grid((3,2),(0,0), colspan=2, rowspan=2)
	plt.text(0.5, 1.05, "Number of TRAP Laws", transform = ax_mainland.transAxes)
	ax_mainland.axis("off")

	#map for the lower 48
	colors = {}
	state_names = []
	for shapedict in map_lower_48.states_info:
		state = shapedict['NAME']
		if state != 'Puerto Rico' and state != 'District of Columbia':
			colors[state] = cmap(d[state]) #maps the colors to the states in a dictionary called "colors"
		state_names.append(state)

	for nshape, seg in enumerate(map_lower_48.states):
		state = state_names[nshape]
		if state != 'Puerto Rico' and state != 'District of Columbia':
			color = rgb2hex(colors[state]) 
			mainland_poly = Polygon(seg, facecolor=color, edgecolor=color) 
			ax_mainland.add_patch(mainland_poly)
	map_lower_48.drawstates(color=color, linewidth=0)

	#Repeat for Alaska
	colors = {}
	ax_alaska = plt.subplot2grid((3,2), (2,0), colspan = 1, rowspan=1)
	#ax_alaska.set_title('Alaska')
	ax_alaska.axis("off") #prevents border around state

	for shapedict in m_alaska.states_info:
		colors['Alaska'] = cmap(d['Alaska'])
		state_names.append('Alaska')

	for nshape, seg in enumerate(m_alaska.states):
		color_alaska = rgb2hex(colors['Alaska'])
		alaska_poly = Polygon(seg, facecolor=color_alaska, edgecolor=color_alaska)
		ax_alaska.add_patch(alaska_poly)
	m_alaska.drawstates(color=color, linewidth=0)

	#Repeat for Hawaii
	colors = {}
	ax_hawaii = plt.subplot2grid((3,2), (2,1), colspan = 1, rowspan=1)  
	#ax_hawaii.set_title('Hawaii')
	ax_hawaii.axis("off")

	for shapedict in m_hawaii.states_info:
		colors['Hawaii'] = cmap(d['Hawaii'])
		state_names.append('Hawaii')

	for nshape, seg in enumerate(m_hawaii.states):
		color_hawaii = rgb2hex(colors['Hawaii'])
		hawaii_poly = Polygon(seg, facecolor=color_hawaii, edgecolor=color_hawaii)
		ax_hawaii.add_patch(hawaii_poly)
		
	m_hawaii.drawstates(color=color_hawaii, linewidth=0)

	plt.show()
	#plt.savefig('state_name_scores.png', dpi=300) #bbox_inces='tight')

# make a colormap of states according to how many TRAP laws they have
def plot_state_traplaws():
	d = {}
	for s in lawsdata.state:
		d[s] = int(lawsdata.test[lawsdata.state == s]*2)

	make_statemap(d)

# plot a heatmap of driving time to nearest clinic for each state
def plot_drivetime_heatmap():

	m = Basemap(llcrnrlon=-119,llcrnrlat=22,urcrnrlon=-64,urcrnrlat=49,  
	                projection='lcc',lat_1=33,lat_2=45,lon_0=-95)

	states_shp_info = m.readshapefile('shapefiles/st99_d00', 'states',drawbounds=True)

	x,y = m(cities['lng'].values, cities['lat'].values)
	vals = cities['drivetime'].values
	vals = [v/60.0 for v in vals] # values are hours

	m.scatter(x,y, c=vals, cmap='jet', vmin=0, vmax=5, lw=0)
	m.drawstates(linewidth=0)
	plt.colorbar()

	# Show the map
	plt.show()

plot_drivetime_heatmap()