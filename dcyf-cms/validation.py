"""
Check input JSON against Ohana API JSON
as defined at
https://github.com/codeforamerica/ohana-api/wiki/Populating-the-Postgres-database-from-a-JSON-file

See http://www.alexconrad.org/2011/10/json-validation.html

This may not report additional fields that do not match the schema.
"""
import json
import sys

import validictory

SCHEMA = {
    "properties": {'name': {'type': 'string'}}
}
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


def read_json(filepath):
    with open(filepath, 'rb') as f:
        data = json.load(f)
    return data


if __name__ == '__main__':
    # Output whether input filename conforms to the file format
    try:
        filename = sys.argv[1]
    except IndexError:
        print "Usage: python validation.py <filename.json>"
        sys.exit(1)
    data = read_json(filename)
    try:
        validictory.validate(data, SCHEMA)
    except ValueError as ex:
        print ex
    else:
        print 'JSON validated'
