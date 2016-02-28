import urllib2
import json
import csv

def getRow(data):
    # ?? this totally depends on what's in your data
    pass

url = "http://abortiondocs.org/search-results/?clinic_type=1&ajax=true&query=SResultsMap"
data = urllib2.urlopen(url).read()
data = json.loads(data)

# fname = "mydata.csv"
# with open(fname,'wb') as outf:
#     outcsv = csv.writer(outf)
#     outcsv.writerows(getRows(data))

print data

f = csv.writer(open("ablocs.csv", "wb+"))

# Write CSV Header, If you dont need that, remove this line
f.writerow(["name", "city", "state", "zip", "latitude", "longitude"])

for x in data:
    f.writerow([x["name"],
    			x["city"], 
                x["state"], 
                str(x["zip"]), 
                x["latitude"],
                x["longitude"]])