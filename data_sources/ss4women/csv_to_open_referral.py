import json, csv, re

import nltk

class Entry:
    pass


def read_csv(filename):
    
    # Read the passed csv file into a list of objects.

    with open(filename, 'r') as f:
        reader = csv.reader(
            f, delimiter=',', quotechar='"', skipinitialspace=True)
        rows = [row for row in reader]
    entries = []
    if rows:
        keys = rows[0]
        keys = [key.strip().lower().replace(' ', '_') for key in keys]
        print 'keys:', keys
        for row in rows[1:]:
            entry = Entry()
            for key, val in zip(keys, row):
                setattr(entry, key, val)
            entries.append(entry)
    return entries

'''
csv columns
"Organization Name", "Address", "Phone", "Fax", "Email", "Website", "Contact", 
"Age Groups", "Languages Spoken", "Fees", "Service Hours", "Services Provided"
'''

sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

def to_open_referral(entry):

    # Default values.

    city, state, zip, = '', '', ''
    languages = entry.languages_spoken
    short_description = entry.services_provided[:100]
    name, title = entry.contact, ''

    # Apply fanciness.

    if ', San Francisco' in entry.address:
        entry.address = entry.address.replace(', San Francisco', '')
        city = 'San Francisco'
    if ', CA' in entry.address:
        entry.address = entry.address.replace(', CA', '')
        state = 'CA'
    zip_regex = '( [0-9]{5})$'
    match = re.search(zip_regex, entry.address)
    if match:
        zip = match.group(0).strip()
        entry.address = re.sub(zip_regex, '', entry.address)
    languages = languages.replace(' and ', '').split(', ')
    if ',' in name:
        name, title = [s.strip() for s in name.rsplit(',', 1)]

    short_description = sent_detector.tokenize(
        entry.services_provided.strip())[0]

    # Fill in the blanks.

    return {
        'name':entry.organization_name,
        'locations':[
            {
                'name':entry.organization_name,  
                'contacts_attributes':[  
                    {
                        'name':name,  
                        'title':title,  
                    }
                ],
                'description':entry.services_provided,
                'short_description':short_description,
                'address_attributes':{
                    'street': entry.address,
                    'city': city,
                    'state': state,
                    'zip': zip
                },
                "mail_address_attributes": {
                    "attention": entry.organization_name,
                    "street": entry.address,
                    "city": city,
                    "state": state,
                    "zip": zip
                },
                "hours": entry.service_hours,
                "transportation": "",
                "accessibility": [
                ],
                "languages":languages,
                "emails": [
                    entry.email.split(', ')
                ],
                "faxes_attributes": [
                    {
                        "number": entry.fax
                    }
                ],
                "phones_attributes": [
                    {
                        "number": entry.phone
                    }
                ],
                "urls": [
                    entry.website
                ],
                "services_attributes": [
                    {
                        "audience": "",
                        "eligibility": entry.age_groups,
                        "fees": entry.fees,
                        "how_to_apply": "",
                        "service_areas": [],
                        "keywords": [],
                        "wait": "",
                        "funding_sources": []
                    }
                ],
            }
        ],
    }


entries = read_csv('directory.csv')[100:200]

entries = [to_open_referral(entry) for entry in entries]
with open('open_ref.json', 'w') as f:
    out_data = json.dumps(entries, indent=2, ensure_ascii=False)
    f.write(out_data)




