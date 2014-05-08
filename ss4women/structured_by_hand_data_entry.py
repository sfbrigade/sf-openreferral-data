import json
<<<<<<< HEAD
import csv

def getField(fieldValue, fieldName):
    try:
        fieldValue = fieldValue[0]
    except:
        pass
    result = fieldValue
    isCorrect = raw_input('\n%s correct?: %s (y/n) >> ' % (fieldName, fieldValue))
    if isCorrect != 'y':
        result = raw_input("\n%s? >> " % fieldName)
    return result

fileIn = csv.reader(open('directory.csv'), delimiter=',', quotechar='"', skipinitialspace=True)
next(fileIn)
for line in fileIn:
    g = open('output.json', 'a')
    names = line[0].split(',')
    locations = line[1]
    phoneNumbers = line[2].split(',')
    faxNumbers = line[3].split(',')
    possibleEmails = line[4].split(',')
    possibleURLs = line[5].split(',')
    print('\n')
    print('---------- NEXT ---------------')
    print(line,)
    organization_name = getField(names, 'name')
    print('\n')
    org = {"name": str(organization_name)}

    print('Possible Location(s): ', locations)
    location_flag = raw_input("\nDoes it have a location (y/n)>> ")
    if location_flag != 'n':
        locs = []
        while location_flag != 'n':
            location_name = raw_input("\nLocation name? >> ")
            location = {"name": str(location_name)}
            street = raw_input("\nStreet address? >> ")
            city = raw_input("\nCity? >> ")
            state = raw_input("\nState? >> ")
            zipcode = raw_input("\nZipcode? >> ")
            address = {
                "street": str(street),
                "city": str(city),
                "state": str(state),
                "zipcode": str(zipcode)
            }
            location["address"] = address

            print('Possible Emails: %s' % possibleEmails)
            email_flag = raw_input("\nDo they have an email? (y/n) >> ")
            if email_flag != 'n':
                emails = []
                while email_flag != 'n':
                    email = getField(possibleEmails, 'Email')
                    # email = raw_input("\nEmail? >> ")
                    emails.append(str(email))
                    email_flag = raw_input("\nDo they have another email? (y/n) >> ")
                    print('\n')

                location['emails'] = emails

            print('Possible Websites: %s' % possibleURLs)
            url_flag = raw_input("\nDo they have a website? (y/n) >> ")
            if url_flag != 'n':
                urls = []
                while url_flag != 'n':
                    url = getField(possibleURLs, '\nURL? (include http:// or https://)')
                    # url = raw_input("\nURL? (include http:// or https://) >> ")
                    urls.append(str(url))
                    url_flag = raw_input("\nDo they have another url? (y/n) >> ")
                    print('\n')

                location['urls'] = urls

            print('Possible Phone Numbers: %s' % phoneNumbers)
            phone_flag = raw_input("\nDo they have a phone number? (y/n) >> ")
            if phone_flag != 'n':
                phones = []
                while phone_flag != 'n':
                    # number = raw_input("\nPhone #? [ex. 123 456-7890] >> ")
                    number = getField(phoneNumbers, "\nPhone #? [ex. 123 456-7890] >> ")
                    phone = {"number": str(number)}
                    vanity_number = raw_input("\nVanity number? (press enter to skip) >> ")
                    if vanity_number:
                        phone['vanity_number'] = str(vanity_number)
                        vanity_number = ''
                    phone_department = raw_input("\nDepartment? (press enter to skip) >> ")
                    if phone_department:
                        phone['department'] = str(phone_department)
                        phone_department = ''
                    extension = raw_input("\nExtension? (ex. x1234) Press enter to skip >> ")
                    if extension:
                        phone['extension'] = str(extension)
                        extension = ''
                    phone_type = raw_input("Type (TTY, etc)? Press enter to skip >> ")
                    if phone_type:
                        phone['type'] = str(phone_type)
                        phone_type = ''
                    phones.append(phone)
                    phone_flag = raw_input("Add another phone number? (y/n) >> ")
                    print('\n')

                location['phones'] = phones

            contact_flag = raw_input("\nIs there a contact person? (y/n) >> ")
            if contact_flag != 'n':
                contacts = []
                while contact_flag != 'n':
                    name = raw_input("\nName? >> ")
                    contact = {"name": str(name)}
                    title = raw_input("\nWhat is their title? (press enter to skip) >> ")
                    if title:
                        contact['title'] = str(title)
                        title = ''
                    contact_email = raw_input("\nWhat is their email address? (press enter to skip) >> ")
                    if contact_email:
                        contact['email'] = str(contact_email)
                        contact_email = ''
                    contact_fax = raw_input("\nWhat is their fax number? (press enter to skip) >> ")
                    if contact_fax:
                        contact['fax'] = contact_fax
                        contact_fax = ''
                    contact_phone = raw_input("\nPhone number w/o extension, e.g. 123 456-7890? (press enter to skip) >> ")
                    if contact_phone:
                        contact['phone'] = contact_phone
                        contact_phone = ''
                    contact_extension = raw_input("\nExtension, e.g. x1234? (press enter to skip) >> ")
                    if contact_extension:
                        contact['extension'] = contact_extension
                        contact_extension = ''
                    contacts.append(contact)
                    contact_flag = raw_input("\nIs there another contact person? (y/n) >> ")

                location['contacts'] = contacts

            print("Possible Fax Numbers: %s" % faxNumbers)
            fax_flag = raw_input("\nDo they have a fax number? (y/n) >> ")
            if fax_flag != 'n':
                faxes = []
                while fax_flag != 'n':
                    # number = raw_input("\nFax #? [ex. 123 456-7890] >> ")
                    number = getField(faxNumbers, "\nFax #? [ex. 123 456-7890] >> ")
                    fax = {"number": str(number)}
                    department = raw_input("\nWhat department will it go to? (press enter to skip) >> ")
                    if department:
                        fax['department'] = str(department)
                    faxes.append(phone)
                    fax_flag = raw_input("Add another fax number? (y/n) >> ")

                location['faxes'] = faxes

            hours = raw_input("\nHours? (press enter to skip) >> ")
            if hours:
                location['hours'] = hours

            language_flag = raw_input("\nDo they have languages specified? (y/n) >> ")
            if language_flag != 'n':
                languages = []
                while language_flag != 'n':
                    language = raw_input("\nLanguage (one at a time)? >> ")
                    languages.append(str(language))
                    language_flag = raw_input("\nAdd another language? (y/n) >> ")

                location['languages'] = languages

            short_desc = raw_input("\nShort description? >> ")
            location['short_desc'] = str(short_desc)
            description = raw_input("\nLong description? >> ")
            location['description'] = str(description)
            locs.append(location)
            location_flag = raw_input('\nAdd another location? (y/n) >> ')

        org['locs'] = locs
    audience = raw_input('\nWhat is the target age group? (press enter to skip) >> ')
    if audience:
        try:
            org['servs']['audience'] = str(audience)
        except:
            org['servs'] = {'audience': str(audience)}

    fees = raw_input('\nWhat are the fees? (press enter to skip) >> ')
    if fees:
        try:
            org['servs']['fees'] = str(fees)
        except:
            org['servs'] = {'fees': str(fees)}
    try:
        has_loc = org['locs']
    except:
        try:
            servs = org['servs']
        except:
            org['servs'] = {}
            servs = org['servs']
        servs['short_desc'] = str(raw_input('\nShort Description? >> '))
        servs['desciption'] = str(raw_input('\nDescription? >> '))
        url_flag = raw_input('\nDo they have a website? (y/n) >> ')
=======
g = open('output.json', 'a')
organization_name = raw_input("\nName? >> ")
org = {"name": str(organization_name)}
location_flag = raw_input("\nDoes it have a location (y/n)>> ")
if location_flag != 'n':
    locs = []
    while location_flag != 'n':
        location_name = raw_input("\nLocation name? >> ")
        location = {"name": str(location_name)}
        street = raw_input("\nStreet address? >> ")
        city = raw_input("\nCity? >> ")
        state = raw_input("\nState? >> ")
        zipcode = raw_input("\nZipcode? >> ")
        address = {
            "street": str(street),
            "city": str(city),
            "state": str(state),
            "zipcode": str(zipcode)
        }
        location["address"] = address
        email_flag = raw_input("\nDo they have an email? (y/n) >> ")
        if email_flag != 'n':
            emails = []
            while email_flag != 'n':
                email = raw_input("\nEmail? >> ")
                emails.append(str(email))
                email_flag = raw_input("\nDo they have another email? (y/n) >> ")

            location['emails'] = emails

        url_flag = raw_input("\nDo they have a website? (y/n) >> ")
>>>>>>> 8eb1bbb8d262a29ecf7beb17fc144faba88e2def
        if url_flag != 'n':
            urls = []
            while url_flag != 'n':
                url = raw_input("\nURL? (include http:// or https://) >> ")
                urls.append(str(url))
                url_flag = raw_input("\nDo they have another url? (y/n) >> ")
            urls.append(url)
            servs['urls'] = urls

<<<<<<< HEAD
    g.write(json.dumps(org) + ',')
    g.close()
=======
            location['urls'] = urls

        phone_flag = raw_input("\nDo they have a phone number? (y/n) >> ")
        if phone_flag != 'n':
            phones = []
            while phone_flag != 'n':
                number = raw_input("\nPhone #? [ex. 123 456-7890] >> ")
                phone = {"number": str(number)}
                vanity_number = raw_input("\nVanity number? (press enter to skip) >> ")
                if vanity_number:
                    phone['vanity_number'] = str(vanity_number)
                    vanity_number = ''
                phone_department = raw_input("\nDepartment? (press enter to skip) >> ")
                if phone_department:
                    phone['department'] = str(phone_department)
                    phone_department = ''
                extension = raw_input("\nExtension? (ex. x1234) Press enter to skip >> ")
                if extension:
                    phone['extension'] = str(extension)
                    extension = ''
                phone_type = raw_input("Type (TTY, etc)? Press enter to skip >> ")
                if phone_type:
                    phone['type'] = str(phone_type)
                    phone_type = ''
                phones.append(phone)
                phone_flag = raw_input("Add another phone number? (y/n) >> ")

            location['phones'] = phones

        contact_flag = raw_input("\nIs there a contact person? (y/n) >> ")
        if contact_flag != 'n':
            contacts = []
            while contact_flag != 'n':
                name = raw_input("\nName? >> ")
                contact = {"name": str(name)}
                title = raw_input("\nWhat is their title? (press enter to skip) >> ")
                if title:
                    contact['title'] = str(title)
                    title = ''
                contact_email = raw_input("\nWhat is their email address? (press enter to skip) >> ")
                if contact_email:
                    contact['email'] = str(contact_email)
                    contact_email = ''
                contact_fax = raw_input("\nWhat is their fax number? (press enter to skip) >> ")
                if contact_fax:
                    contact['fax'] = contact_fax
                    contact_fax = ''
                contact_phone = raw_input("\nPhone number w/o extension, e.g. 123 456-7890? (press enter to skip) >> ")
                if contact_phone:
                    contact['phone'] = contact_phone
                    contact_phone = ''
                contact_extension = raw_input("\nExtension, e.g. x1234? (press enter to skip) >> ")
                if contact_extension:
                    contact['extension'] = contact_extension
                    contact_extension = ''
                contacts.append(contact)
                contact_flag = raw_input("\nIs there another contact person? (y/n) >> ")

            location['contacts'] = contacts

        fax_flag = raw_input("\nDo they have a fax number? (y/n) >> ")
        if fax_flag != 'n':
            faxes = []
            while fax_flag != 'n':
                number = raw_input("\nFax #? [ex. 123 456-7890] >> ")
                fax = {"number": str(number)}
                department = raw_input("\nWhat department will it go to? (press enter to skip) >> ")
                if department:
                    fax['department'] = str(department)
                faxes.append(phone)
                fax_flag = raw_input("Add another fax number? (y/n) >> ")

            location['faxes'] = faxes

        hours = raw_input("\nHours? (press enter to skip) >> ")
        if hours:
            location['hours'] = hours

        language_flag = raw_input("\nDo they have languages specified? (y/n) >> ")
        if language_flag != 'n':
            languages = []
            while language_flag != 'n':
                language = raw_input("\nLanguage (one at a time)? >> ")
                languages.append(str(language))
                language_flag = raw_input("\nAdd another language? (y/n) >> ")

            location['languages'] = languages

        short_desc = raw_input("\nShort description? >> ")
        location['short_desc'] = str(short_desc)
        description = raw_input("\nLong description? >> ")
        location['description'] = str(description)
        locs.append(location)
        location_flag = raw_input('\nAdd another location? (y/n) >> ')

    org['locs'] = locs
audience = raw_input('\nWhat is the target age group? (press enter to skip) >> ')
if audience:
    try:
        org['servs']['audience'] = str(audience)
    except:
        org['servs'] = {'audience': str(audience)}

fees = raw_input('\nWhat are the fees? (press enter to skip) >> ')
if fees:
    try:
        org['servs']['fees'] = str(fees)
    except:
        org['servs'] = {'fees': str(fees)}
try:
    has_loc = org['locs']
except:
    try:
        servs = org['servs']
    except:
        org['servs'] = {}
        servs = org['servs']
    servs['short_desc'] = str(raw_input('\nShort Description? >> '))
    servs['desciption'] = str(raw_input('\nDescription? >> '))
    url_flag = raw_input('\nDo they have a website? (y/n) >> ')
    if url_flag != 'n':
        urls = []
        while url_flag != 'n':
            url = raw_input("\nURL? (include http:// or https://) >> ")
            urls.append(str(url))
            url_flag = raw_input("\nDo they have another url? (y/n) >> ")
        urls.append(url)
        servs['urls'] = urls

g.write(json.dumps(org) + ',')
g.close()
>>>>>>> 8eb1bbb8d262a29ecf7beb17fc144faba88e2def
