### color_map.py
 
import csv
# from BeautifulSoup import BeautifulSoup
from bs4 import BeautifulSoup 
# Read in unemployment rates

from constant import abbrevs

plot_dict = {}
# min_value = 100; max_value = 0
abbrevs['DC'] = "Washington"

abbrevs_inverted = dict((v,k) for k,v in abbrevs.iteritems())

reader = csv.reader(open('Abortion_in_States.csv'), delimiter=",")


firstTime = True
rate_list = []
for row in reader:
	if firstTime:
		firstTime = False
		continue
	rate = int(row[8][:-5].strip())
	rate_list.append(rate)
	state = str(row[0][2:])
	state_abbrev = abbrevs_inverted[state]
	plot_dict[state_abbrev] = rate

# # Load the SVG map
svg = open('States.svg', 'r').read()
 
# # Load into Beautiful Soup
soup = BeautifulSoup(svg, selfClosingTags=['defs','sodipodi:namedview'])
 
# # Find counties
paths = soup.findAll('path')

 

# # Map colors
colors = ["#F1EEF6", "#D4B9DA", "#C994C7", "#DF65B0", "#DD1C77", "#980043"]
 
# # County style
path_style = "font-size:12px;fill-rule:nonzero;stroke:#FFFFFF;stroke-opacity:1; stroke-width:0.1;stroke-miterlimit:4;stroke-dasharray:none;stroke-linecap:butt; marker-start:none;stroke-linejoin:bevel; fill:"
 
min_rate = min(rate_list)
max_rate = max(rate_list)

counter = 0
# # Color the counties based on unemployment rate
for p in paths:
	try:
		if p['id'] not in ["State_Lines", "separator"]:
			rate = plot_dict[p['id']]
			color_class = int((len(colors)-1) * float(rate - min_rate) / float(max_rate - min_rate))
			# print "color_class"
			# print color_class
			color = colors[color_class]
			# print "color"
			# print color
			p['style'] = path_style + color
 	except:
 		counter += 1
 		# print counter 
 		pass
print soup.prettify()
