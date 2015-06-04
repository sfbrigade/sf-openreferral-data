"""
Convert DCYF-CMS CSV to Ohana API JSON
as defined at
https://github.com/codeforamerica/ohana-api/wiki/Populating-the-Postgres-database-from-a-JSON-file
Read dcyf_cms_05312013.csv
Transform to match the Ohana spec
Write to JSON

"""
from collections import defaultdict
import csv
import json
import os
import sys


class Entry(object):
    """Represents a record for service location"""
    # TODO: flesh this out
    def __init__(self):
        self.org_name = None
        self.loc = None


def read_csv(csv_file_name):
    """Converts a csv of organizations into a tuple of dicts"""
    with open(csv_file_name, 'rb') as csvfile:
        return tuple(csv.DictReader(csvfile, dialect='excel'))


def make_entries(lines_from_csv):
    """Placeholder function"""
    entries = []
    for line in lines_from_csv:
        entry = Entry()
        entry.org_name = line['Agency Name']
        entry.loc = line['Program Name']
        entries.append(entry)
    return entries


def entries_to_dicts(per_location_entries):
    """Placeholder function"""
    org_dict = defaultdict(list)
    for entry in per_location_entries:
        org_dict[entry.org_name].append({'name': entry.org_name,
                                         'loc': entry.loc})
    return org_dict


# TODO: use this template as a model for how to create JSON
# template = {
#         'name':entry.organization_name,
#         'locations':[
#             {
#                 'name':entry.organization_name,
#                 'contacts_attributes':[
#                     {
#                         'name':name,
#                         'title':title,
#                     }
#                 ],
#                 'description':entry.services_provided,
#                 'short_description':short_description,
#                 'address_attributes':{
#                     'street': entry.address,
#                     'city': city,
#                     'state': state,
#                     'zip': zip
#                 },
#                 "mail_address_attributes": {
#                     "attention": entry.organization_name,
#                     "street": entry.address,
#                     "city": city,
#                     "state": state,
#                     "zip": zip
#                 },
#                 "hours": entry.service_hours,
#                 "transportation": "",
#                 "accessibility": [
#                 ],
#                 "languages":languages,
#                 "emails": [
#                     entry.email.split(', ')
#                 ],
#                 "faxes_attributes": [
#                     {
#                         "number": entry.fax
#                     }
#                 ],
#                 "phones_attributes": [
#                     {
#                         "number": entry.phone
#                     }
#                 ],
#                 "urls": [
#                     entry.website
#                 ],
#                 "services_attributes": [
#                     {
#                         "audience": "",
#                         "eligibility": entry.age_groups,
#                         "fees": entry.fees,
#                         "how_to_apply": "",
#                         "service_areas": [],
#                         "keywords": [],
#                         "wait": "",
#                         "funding_sources": []
#                     }
#                 ],
#             }
#         ],
#     }


if __name__ == '__main__':
    # Convert DCYF-CMS CSV to Ohana API JSON
    try:
        filename = sys.argv[1]
    except IndexError:
        print "Usage: python validation.py <filename.json>"
        sys.exit(1)
    data = read_csv(filename)
    entries = make_entries(data)
    output = entries_to_dicts(entries)
    output_filename = "{0}.json".format(
        os.path.splitext(os.path.basename(filename))[0])
    with open(output_filename, 'wb') as f:
        f.write(json.dumps(output, ensure_ascii=False, indent=2))  # Quick fix for non-ASCII characters
    print 'CSV converted to JSON'
