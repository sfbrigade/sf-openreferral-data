import re
from csv import reader

# A lot of these functions do nothing other than simply output their input.
# The code is structured this way for clarity and ease-of-editing later on
# in case we want to change the structure

def parse_contact_field(field, g):
    field = field.strip()
    field = field.split(';')
    contacts = []
    for elem in field:
        elem = elem.split(',')
        if re.search(r'\.org|On website|Receptionist', elem[0]):
            continue
        else:
            if re.search(r'\(\d{3}\).\d{3}.\d{4}', elem[0]):
                match = re.search(r'\(\d{3}\).\d{3}.\d{4}', elem[0]).group()
                subbed = re.sub(r'\(\d{3}\).\d{3}.\d{4}', r'', elem[0])
                subbed = re.sub(r'\(ACCESS\):|\(TAP\):', r'', subbed)
                person = {
                        'phone': match.strip(),
                        'name': subbed.strip()
                        }
            else:
                person = {
                    'name': elem[0].strip(),
                }
            for i, section in enumerate(elem):
                if re.search(r'@', section):
                    person['email'] = section.strip()
                if re.search(r'\(\d{3}\).\d{3}.\d{4}', section):
                    match = re.search(r'\(\d{3}\).\d{3}.\d{4}', section).group()
                    person['phone'] = match
                    if i == 1:
                        section = re.sub(r'\(\d{3}\).\d{3}.\d{4}', r'', section)
                        person['title'] = section.strip()
                if re.search(r'x\d+|ex...\d+|EX \d+', section):
                    match = re.search(r'x\d+|ex...\d+|EX \d+', section).group()
                    person['extension'] = 'x' + re.search(r'\d+', match).group()
                    if i == 1:
                        section = re.sub(r'x\d+|ex...\d+|EX \d+', r'', section)
                        person['title'] = section.strip()
            if person.get('title','') == '' and len(elem)>1:
                if re.search('RPN|LCSW', elem[1]) and len(elem) == 2:
                    pass
                elif re.search(r'Ph\.D\.|M\.S\.W\.|LCSW', elem[1]):
                    person['title'] = elem[2].strip()
                else:
                    person['title'] = elem[1].strip()

        contacts.append(person)
    return contacts

# Output the full description
def parse_description(desc):
    return desc

# Output just the first sentence of the description
def parse_short_desc(desc):
    return '.'.join(desc.split('.'))[0]

# Output the hours string
def parse_hours(hours):
    return hours

def parse_languages(langs):
    return lang.split(',')

# Each ss has one url
def parse_url(url):
    return url

f = reader(open('phone_numbers.csv'))
g = open('test_results.csv', 'w+')

def parse_phones(phones):
    phones = phones.split(',')
    numbers = []
    print phones
    for num in phones:
        numbers.append({'number': num})
    return numbers

for line in f:
    results = parse_phones(line)
    g.write(results + '\n')

g.close()

def parse(read):
    orgs = {}
    for line in read:
        org = orgs.get(line[0],{})
        org['name'] = line[0]
        locs = org.get('locs',[])
        loc = {
            #'name': #TODO,
            'contacts': [

            ]

        }


if __name__ == '__main__':
    read = reader(open('directory.csv'), delimiter=',',
        quotechar='"', skipinitialspace=True)
    parse(read)
