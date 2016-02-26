from bs4 import BeautifulSoup
import urllib2
import csv

site= "http://data.rhrealitycheck.org/"
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

req = urllib2.Request(site, headers=hdr)

try:
    page = urllib2.urlopen(req)
except urllib2.HTTPError, e:
    print e.fp.read()

content = page.read()
#print content
# r = urllib2.urlopen('http://data.rhrealitycheck.org/').read()
# print r
soup = BeautifulSoup(content, "lxml")
#print soup.prettify()[0:1000]

a = soup.find_all("div", class_="state-info")
print a[0].h2.get_text()
print a[0].find_all("tr")[1].td.get_text()

f = csv.writer(open("ablaws.csv", "wb+"))

# Write CSV Header, If you dont need that, remove this line
f.writerow(["state", "numlaws"])

for x in a:
    f.writerow([x.h2.get_text(), 
                x.find_all("tr")[1].td.get_text()])