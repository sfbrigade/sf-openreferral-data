import csv, json
from pprint import pprint
import dateutil.parser
from sys import argv

def csv_dict_writer(path, fieldnames, data):
	"""
	Writes a CSV file using DictWriter
	"""
	with open(path, "wb") as out_file:
		writer = csv.DictWriter(out_file, delimiter=',', fieldnames=fieldnames)
		writer.writeheader()
		for row in data:
			#pprint(row)
			writer.writerow(row)


def main(filename):
	json_data=open('linksf.json')
	#pprint(json_data.read())
	data = json.load(json_data)

	locations = []
	for location in data:
		loc = {}
		loc['name'] = location['name'].encode('utf8')
		loc['lat'] = location['location']['latitude']
		loc['long'] = location['location']['longitude']
		loc['address'] = location['address'].encode('utf8')
		loc['phone'] = location['phone'].encode('utf8')
		loc['notes'] = location['notes'].encode('utf8')
		#print dateutil.parser.parse(location['updatedAt']).date()
		loc['updatedAt'] = dateutil.parser.parse(location['updatedAt']).date().strftime("%m/%d/%Y").encode('utf8')
		for service in location['services']:
			loc['food'] = 0
			loc['technology'] = 0
			loc['housing'] = 0
			loc['medical'] = 0
			loc['hygiene'] = 0
			if service["category"] == "food":
				loc['food'] = 1
			if service["category"] == "technology":
				loc['technology'] = 1
			if service["category"] == "housing":
				loc['housing'] = 1
			if service["category"] == "medical":
				loc['medical'] = 1
			if service["category"] == "hygiene":
				loc['hygiene'] = 1
		locations.append(loc)
	print(len(locations))
	#pprint(locations)
	csv_dict_writer('locations.csv',list(locations[0].keys()),locations)

main(argv[0])