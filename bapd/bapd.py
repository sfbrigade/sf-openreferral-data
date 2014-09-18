import json
import sys

# Ohana Data Organization
# org 
#	name
#	urls
#	locs
#		name
#		address
#			street
#			city
#			state
#			zipcode
#		phones
#			number
#		urls
#		short_desc
#		description
#		service_attributes
#			how_to_apply
#			eligibility

# Bay Area Progressive Directory (bapd) Data Organization
# Directory Download Location: http://bapd.org/dirdbinfo.html
# Download directory into tab delimited txt file - default name bapd_groups.txt
#
# nameLast nameFirst nameAlt preAddress crossStreet
# address city state zip voice fax
# notes internalNotes keys
# entryDate verifyDate verifyMethod email web
#


# Open output file
g = open('bapd.json', 'w')


Filename = raw_input('Please enter the name of the input file: ' )
# Default to my standard name for bapd dataset
if Filename == '':
	Filename = 'bapd_groups.txt'
F = open(Filename, "r")


LineIn = 0
for lineutf8 in F:
# Drop non-utf8 characters from input line
	lineIn = lineutf8.decode('utf-8','ignore')
	line = lineIn.split('\t')
	org = {"name": line[0]}
	if line[1] != '':
		org["name"] = line[1] + " " + line[0]
	org["urls"] = line[18].split()
# Make sure URLs start with http:// 
	for n,i in enumerate(org["urls"]):
		if i.find("http") == -1:
			org["urls"][n] = "http://" + i
		org["urls"][n].replace("(dot)",".")

	org["aka"] = line[2]

	location = {"name" : line[0] }
	location["description"] = line[11]
	addr = { "street" : line[5], "city" : line[6], "state" : line[7], "zipcode" : line[8]}
	if line[3] != '':
		addr["attention"] = line[3]
	location["address"] = addr
	location["emails"] = line[17].split()
#	print location["emails"]
#	for n, i in enumerate(location["emails"]):
#		location["emails"][n].replace("(dot)",".")

	location["faxes"] = {"number" : line[10]}
	location["phones"] = {"number" : line[9]}
	location["service_attributes"] = {"keywords" : line[13]}
	org["locations"] = location

#	For debugging:
#	print org   
#	q = raw_input('Write Y/N?')
#	if q == 'Y':
	g.write(json.dumps(org) + ',' + '\n')

#	t = raw_input('Quit Y/N?')
#	if t == 'Y':
#		break

g.close()
F.close()
print 'Processing Complete'