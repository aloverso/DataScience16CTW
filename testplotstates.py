import matplotlib.cbook as cbook
import matplotlib.pyplot as plt
import pandas
from mpl_toolkits.basemap import Basemap
import numpy as np
from matplotlib.colors import rgb2hex
from matplotlib.patches import Polygon

# tutorial source 
# http://pythontutorialplots.com/pythontutorial-pandas-matplotlib-and-basemap-tutorial-coloring-states-by-baby-name-uniqueness/
# looks useful, not used though:
# http://flowingdata.com/2009/11/12/how-to-make-a-us-county-thematic-map-using-free-tools

def get_maps():
    map_lower_48 = Basemap(llcrnrlon=-119,llcrnrlat=22,urcrnrlon=-64,urcrnrlat=49,  
                projection='lcc',lat_1=33,lat_2=45,lon_0=-95)

    states_shp_info = map_lower_48.readshapefile('st99_d00', 'states',drawbounds=True)

    m_alaska = Basemap(llcrnrlon=-173,llcrnrlat=51,urcrnrlon=-134.45,urcrnrlat=71.34,
                       projection='lcc', lat_0=64, lon_0=-151)

    alaska_shp_info = m_alaska.readshapefile('st99_d00', 'states',drawbounds=True)


    m_hawaii = Basemap(#llcrnrlon=-161,llcrnrlat=21,urcrnrlon=-154,urcrnrlat=22,
                       width=800000, height=500000,
                       projection='lcc', 
                       lat_0=20.525, lon_0=-157.385,
                       lon_1=-158.115, lat_1=17.24,
                       lon_2=-153.479, lat_2=19.663, 
                       )

    hawaii_shp_info = m_hawaii.readshapefile('st99_d00', 'states',drawbounds=True)

    return map_lower_48, m_alaska, m_hawaii

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

data = pandas.read_csv('ablaws.csv')

d = {}
for s in data.state:
    d[s] = int(data.numlaws[data.state == s]*3)

make_statemap(d)