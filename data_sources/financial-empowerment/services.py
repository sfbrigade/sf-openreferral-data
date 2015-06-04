import csv
import json
import pprint
from urlparse import urlparse

if __name__ == '__main__':
    orgs = { }
    org_locations = { }
    with open('services.csv', 'rbU') as csvfile:
        reader = csv.reader(csvfile, dialect='excel')
        for row in reader:
            if row[2] != '':
                # check for org by name
                if row[2] in orgs:
                    org = orgs[row[2]]
                else:
                    org = { }
                    orgs[row[2]] = org
                    org['urls'] = []
                    org['locations'] = []                    
                    org['name'] = row[2]
                
                # check for unique root url
                if row[5] != '':
                    url = urlparse(row[5])
                    url = url.scheme + '://' + url.netloc
                    if url not in org['urls']:
                        org['urls'].append(url)
                    
                # check for unique location
                if org['name'] in org_locations:
                    locations = org_locations[org['name']]
                else:
                    locations = { }
                    org_locations[org['name']] = locations
                if row[3] in locations:
                    location = locations[row[3]]
                else:
                    location = { }
                    locations[row[3]] = location
                    org['locations'].append(location)
                    
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(orgs)
    