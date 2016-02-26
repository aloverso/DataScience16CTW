import matplotlib.cbook as cbook
import matplotlib.pyplot as plt
import pandas
from mpl_toolkits.basemap import Basemap
import numpy as np
from matplotlib.colors import rgb2hex
from matplotlib.patches import Polygon

data = pandas.read_csv('ablaws.csv')

d = {}
for s in data.state:
	d[s] = int(data.numlaws[data.state == s])

map_lower_48 = Basemap(llcrnrlon=-119,llcrnrlat=22,urcrnrlon=-64,urcrnrlat=49,  
            projection='lcc',lat_1=33,lat_2=45,lon_0=-95)


states_shp_info = map_lower_48.readshapefile('st99_d00', 'states',drawbounds=True)

cmap = plt.cm.Blues
vmin = 0; vmax = 1
colors = {}
state_names = []
for shapedict in map_lower_48.states_info:
    state_name = shapedict['NAME']
    if state_name !='Puerto Rico' and state_name != 'District of Columbia':
        score = d[state_name]
        colors[state_name] = cmap(score*3)
    state_names.append(state_name)


ax = plt.axes()
for nshape, seg in enumerate(map_lower_48.states):
    if state_names[nshape] != 'Puerto Rico' and state_names[nshape] != 'District of Columbia':
        color = rgb2hex(colors[state_names[nshape]]) 
        poly = Polygon(seg, facecolor=color, edgecolor=color) 
        ax.add_patch(poly)
map_lower_48.drawstates(color=color, linewidth=0)
plt.title('Num TRAP laws')
plt.colorbar()
plt.show()