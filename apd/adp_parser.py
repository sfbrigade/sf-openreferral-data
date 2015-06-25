from sys import argv
from re import match
import re
import json
import sys

from english_list_parser import EnglishListParser

class Entry:
    pass

def scraper(file):

    #mapping of APD fields to ohana
    imp_words = [
            ['Administration Mailing Address', "address"],
            ['Administrative Office', "address"],
            ['Office location', "address"],
            ['Intake location', "address"],
            ['Mailing Address', "address"],
            ['Main Office', "address"],
            ['Corporate Office', "address"],
            ['24-Hour Hotline', "phone"],
            ['Toll-Free Telephone', "phone"],
            ['General Inquiries', "phone"],          
            ['Emergency Center Phone', "phone"],
            ['Emergency Bed Call-in #', "phone"],
            ['Address', "address"],
            ['Primary Community Served', "audience"],
            ['Notes', "description"],
            ['Info Line', "phone"],
            ['Phone', "phone"],
            ['Main Phone', "phone"],
            ['Intake Phone', "phone"],
            ['Hours', "hours"],
            ['Clinic Hours', "hours"],
            ['Hours/Meeting times', "hours"],
            ['Intake Hours', "hours"],
            ['Drop-in Hours', "hours"],
            ['Program Hours', "hours"],
            ['Specific Intake Days and Times', "hours"],
            ['Days and Hours', "hours"],
            ['TDD', "phone"],
            ['Fax', "fax"],
            ['Email', "emails"],
            ['E-mail', "emails"],
            ['url', "urls"],
            ['Languages Spoken', "languages"],
            ['What to Bring', "how_to_apply"],
            ['Things to Know', "how_to_apply"],
            ['Accessibility', "accessibility"],
            ['Client fees, if any', "fees"],
            ['Client fee, if any', "fees"],
            ['Client fees', "fees"],
            ['Eligible Population', "eligibility"],
            ['Eligible Populations', "eligibility"],
            ['Eligible Population Served', "eligibility"],
            ['Not Eligible', "eligibility"],
            ['Restrictions', "eligibility"],
            ['Direct Services', "keywords"],
            ['Direct Service', "keywords"],
            ['Faith Based', "description"],
            ['Contact Persons', "name"],
            ['Contact Person', "name"],
            ['Contact', "name"],
            ['Person to Contact', "name"],
            ['Intake Days', "hours"],
            ['Facility Hours', "hours"],
            ['Drop-In Clinic Hours', "hours"],
            ['Location', "address"],
            ['Locations', "address"],
            ['Services', "keywords"],
            ['Days and Times', "hours"],
            ['Note', "description"],
            ]
    line_count = 0
    item_count = 1
    not_matched = ''
    record_line_num = 1
    direct_services = ''
    total_words = len(imp_words)
    entries = []

    open('open_ref.json', 'w').close()  #clear out the json file

    for i, line in enumerate(file):   #go line by line
        line = line.strip()           #pull out extra spacing

        
        if (len(line) > 0) and (line.find('Things To Know')) and (line.find('To Get Connected')):  #skip if it's a blank line or contains a known header
            if record_line_num == 1:     #we're at the first line of the file or the first line of a new record, must be the title
                #print "\nBOR " + str(item_count) + " -----------------------------------------------------------------\n"
                #print "Organization Name: " + line + "\n"
                were_at = 0 
                entry = Entry()
                setattr(entry, "eligibility", "")
                setattr(entry, "fees", "")
                setattr(entry, "accessibility", "")
                setattr(entry, "audience", "")
                setattr(entry, "how_to_apply", "")
                setattr(entry, "hours", "")
                setattr(entry, "emails", "")
                setattr(entry, "urls", "")
                setattr(entry, "languages", "")
                setattr(entry, "fax", "")
                setattr(entry, "phone", "")
                setattr(entry, "name", "")
                setattr(entry, "address", "")
                setattr(entry, "audience", "")
                setattr(entry, "description", "")
                setattr(entry, "keywords", "")
                setattr(entry, "organization_name", "")
                setattr(entry, "program_name", "")

                #first line often contains two values, org and program
                for items in line.split("   "):
                    if were_at == 0:
                        print "Organization: " + items + "\n"
                        setattr(entry, "organization_name", items)

                        were_at = were_at + 1
                    else:
                        print "Program: " + items + "\n"
                        setattr(entry, "program_name", items)
                were_at = 0

            elif record_line_num == 2:   #second line is the description...hopefully
                print "Description: " + line + "\n"
                setattr(entry, "description", line)
                print ""
            else:
                matched = False
                
                for count, word in enumerate(imp_words):  #loop through every important word and look for a match on this line  

                    matched = match_with_word(word, line) #test for a match between word and line
                    if(matched):                          #we've got a match
                        
                        label_text = line.split(":")[0] + ':'
                        just_data =  line.replace(label_text,"").strip();

                        setattr(entry, word[1], getattr(entry, word[1]) + just_data.replace(";",",").strip())

                        if word[0].lower() == "direct services":  #are we at the end of the record?
                            direct_services = direct_services + "; " + line
                            print "NOT MATCHED THIS RECORD: " + not_matched    #if so, print the list of non matching data so we can deal with later
                            
                            #TODO - figure out what to do with this extra info that doesn't match a field label

                            #print "\nEOR " + str(item_count) + " -----------------------------------------------------------------\n"
                            print "\n"

                            entries += [entry]

                            item_count = item_count + 1
                            not_matched = ''
                            record_line_num = 0
                        break                              #found a match so break out of loop and go to next word

                if(matched == False):
                    #print "NOT MATCHED: " + line
                    not_matched = not_matched + "\n" + line  #load all of these non-matching lines into one field so we can analyze


            record_line_num += 1
            #print record_line_num

    entries = [to_open_referral(entry) for entry in entries]
    with open('open_ref.json', 'a') as f:
        out_data = json.dumps(entries, indent=2, ensure_ascii=True)
        f.write(out_data)



def match_with_word(word, line):
    word_length = len(word[0])            #check the length of the word

    if line.split(":")[0].lower() == word[0].lower():   
        return True
    else:
        return False

def to_open_referral(entry):
    # Default values.
    city, state, zip, = '', '', ''
    languages = entry.languages
    emails = entry.emails
    short_description = entry.description[:100]
    
    phonePattern = re.compile(r'(\d{3})\D*(\d{3})\D*(\d{4})\D*(\d*)$')
    
    newphone = phonePattern.search(entry.phone) 
    
    newphonebase = ""
    newext = ""
    
    if newphone:
		newphonebase = newphone.group(1) + newphone.group(2) + newphone.group(3)
		newext = newphone.group(4)
	
    newfax = phonePattern.search(entry.fax) 
    
    newfaxbase = ""
    newfaxext = ""
    
    if newfax:
		newfaxbase = newfax.group(1) + newfax.group(2) + newfax.group(3)
		newfaxext = newfax.group(4)
    
    #name, title = entry.contact, ''

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

	if len(entry.program_name.strip()) == 0:
		entry.program_name = entry.organization_name

    languages = EnglishListParser.parse_list(languages)
    emails = EnglishListParser.parse_list(emails)

    commapos = entry.name.find(',')
    fulllen = len(entry.name)

    if commapos > 0:
        contact_name =  entry.name[0:commapos]
        contact_title =  entry.name[commapos+1:fulllen].strip()
    else:
        contact_name =  entry.name
        contact_title = 'NA'

    


    #if ',' in name:
    	#name, title = [s.strip() for s in name.rsplit(',', 1)]

    # short_description = sent_detector.tokenize(
    #     entry.services_provided.strip())[0]

    # Fill in the blanks.
    # Look here for field definitions:  https://github.com/sfbrigade/ohana-api/wiki/Populating-the-Postgres-database-from-a-JSON-file#accessibility
    
    return {
        'name':entry.organization_name,
        'notes':"",
        'locations':[
            {
                'name':entry.program_name,  
                'contacts_attributes':[  
                    {
                        'name':contact_name,   
                        'title':contact_title,    #TODO - need to split out from name based on comma
                    }
                ],
                'description':entry.description,
                'short_desc':short_description,
                'address_attributes':{
                    'street':entry.address ,
                    'city':city ,       #TODO - need to grab out cities other than SF
                    'state':state ,
                    'zip':zip 
                },
                "hours":entry.hours ,
                "accessibility": [
                    entry.accessibility
                ],
                "languages": languages,
                "emails": emails,
                "faxes_attributes": [
                    {
                        "number": newfaxbase
                    }
                ],
                "phones_attributes": [
                    {
                        "number": newphonebase,
                        "extension": newext
                    }
                ],
                "urls": [
                    entry.urls
                ],
                "services_attributes": [
                    {
                        
                        "name": entry.program_name,
                        "description": entry.description,
                        "audience": entry.audience,
                        "eligibility": entry.eligibility,
                        "fees": entry.fees,
                        "how_to_apply": entry.how_to_apply,
                        "keywords": [entry.keywords],    #TODO - wrap items in double quotes.  I think...
                    }
                ],
            }
        ],
    }

if __name__ == '__main__':
    scraper(open(argv[1]))


