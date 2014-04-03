import re
from csv import reader
f = open('contacts.csv');  g = open('split_contacts.csv', 'w+')
def parse_contact_field(field, g):
    field = field.strip()
    field = field.split(';')
    contacts = []
    for elem in field:
        elem = elem.split(',')
        if re.search(r'\.org|On website|Receptionist', elem[0]):
            continue
        else:
            person = {
                'name': elem[0].strip(),
            }
            if len(elem) > 1:
                for i, section in enumerate(elem):
                    if re.search(r'@', section):
                        person['email'] = section.strip()
                    if re.search(r'\(\d{3}\)\ \d{3}-\d{4}', section):
                        match = re.search(r'\(\d{3}\)\ \d{3}-\d{4}', section).group()
                        person['phone'] = match
                        if i == 1:
                            section = re.sub(r'\(\d{3}\)\ \d{3}-\d{4}', r'', section)
                            person['title'] = section.strip()
                    if re.search(r'x\d+|ex...\d+|EX \d+', section):
                        match = re.search(r'x\d+|ex...\d+|EX \d+', section).group()
                        person['extension'] = 'x' + re.search(r'\d+', match).group()
                        if i == 1:
                            section = re.sub(r'x\d+|ex...\d+|EX \d+', r'', section)
                            person['title'] = section.strip()
                if person.get('title','') == '':
                    person['title'] = elem[1].strip()


        contacts.append(person)
    g.write(str(contacts) + '\n')

for line in f:
    if line.strip(' \n'):
        g.write(line.strip() + '\n')

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


#if __name__ == '__main__':
#    read = reader(open('directory.csv'), delimiter=',',
#        quotechar='"', skipinitialspace=True)
#    parse(read)
