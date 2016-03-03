import geocoder
pop = geocoder.population('Springfield, Virginia')
print pop

# import simplejson as json
# import json
# g = geocoder.google('Ottawa, ON')
# print json.dumps(g.geojson, indent=4)
# g = geocoder.geonames('Ottawa, ON')
# print g.json


# import geocoder
# g = geocoder.geonames('New York City', username='<zwang>')
# print g.json