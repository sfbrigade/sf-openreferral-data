from sys import argv
from re import match
import re
import json
import sys

class Entry:
    pass

def scraper(file):

#"Organization Name", "Program", "Address", "Phone", "Fax", "Email", "Website", "Contact", "Age Groups", "Languages Spoken", "Fees", "Service Hours", "Services Provided"

    imp_words = [
            ['Administration Mailing Address', "Address"],
            ['Administrative Office', "Address"],
            ['Office location', "Address"],
            ['Intake location', "Address"],
            ['Mailing Address', "Address"],
            ['Main Office', "Address"],
            ['Corporate Office', "Address"],
            ['24-Hour Hotline', "Phone"],
            ['Toll-Free Telephone', "Phone"],
            ['General Inquiries', "Phone"],          
            ['Emergency Center Phone', "Phone"],
            ['Emergency Bed Call-in #', "Phone"],
            ['Address', "Address"],
            ['Primary Community Served', "audience"],
            ['Notes', "description"],
            ['Info Line', "Phone"],
            ['Phone', "Phone"],
            ['Main Phone', "Phone"],
            ['Intake Phone', "Phone"],
            ['Hours', "hours"],
            ['Clinic Hours', "hours"],
            ['Hours/Meeting times', "hours"],
            ['Intake Hours', "hours"],
            ['Drop-in Hours', "hours"],
            ['Program Hours', "hours"],
            ['Specific Intake Days and Times', "hours"],
            ['Days and Hours', "hours"],
            ['TDD', "Phone"],
            ['Fax', "number"],
            ['Email', "emails"],
            ['E-mail', "emails"],
            ['url', "urls"],
            ['Languages Spoken', "languages"],
            ['What to Bring', "how_to_apply"],
            ['Things to Know', "how_to_apply"],
            ['Accessibility', "accessibility"],
            ['Client fees, if any', "Fees"],
            ['Client fee, if any', "Fees"],
            ['Client fees', "Fees"],
            ['Eligible Population', "eligibility"],
            ['Eligible Populations', "eligibility"],
            ['Eligible Population Served', "eligibility"],
            ['Not Eligible', "eligibility"],
            ['Restrictions', "eligibility"],
            ['Direct Services', "keywords"],
            ['Direct Service', "keywords"],
            ['Faith Based', ""],
            ['Contact Persons', "name"],
            ['Contact Person', "name"],
            ['Contact', "name"],
            ['Person to Contact', "name"],
            ['Intake Days', "hours"],
            ['Facility Hours', "hours"],
            ['Drop-In Clinic Hours', "hours"],
            ['Location', "Address"],
            ['Locations', "Address"],
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

    setattr(entry, "eligibility", "")
    setattr(entry, "fees", "")
    
    open('open_ref.json', 'w').close()


    for i, line in enumerate(file):   #go line by line
        line = line.strip()           #pull out extra spacing

        
        if (len(line) > 0) and (line.find('Things To Know')) and (line.find('To Get Connected')):  #skip if it's a blank line or contains a known header
            if record_line_num == 1:     #we're at the first line of the file or the first line of a new record, must be the title
                #print "\nBOR " + str(item_count) + " -----------------------------------------------------------------\n"
                #print "Organization Name: " + line + "\n"
                were_at = 0 
                entry = Entry()


                for items in line.split("   "):
                    if were_at == 0:
                        print "Organization: " + items + "\n"
                        setattr(entry, "organization_name", items)
                        were_at = were_at + 1
                    else:
                        print "Program: " + items + "\n"
                        setattr(entry, "organization_name", items)
                were_at = 0

            elif record_line_num == 2:   #second line is the description...hopefully
                print "Description: " + line + "\n"
                print ""
            else:
                matched = False
                
                for count, word in enumerate(imp_words):  #loop through every important word and look for a match on this line  

                    matched = match_with_word(word, line) #test for a match between word and line
                    if(matched):                          #we've got a match
                        
                        label_text = line.split(":")[0] + ':'
                        just_data = line.replace(label_text,"").strip();
                 
                        setattr(entry, word[1], just_data.replace(";",",").strip())

                        if word[0].lower() == "direct services":  #are we at the end of the record?
                            direct_services = direct_services + "; " + line
                            print "NOT MATCHED THIS RECORD: " + not_matched    #if so, print the list of non matching data so we can deal with later
                            #print "\nEOR " + str(item_count) + " -----------------------------------------------------------------\n"
                            print "\n"


                            output = to_open_referral(entry)
                            with open('open_ref.json', 'a') as f:
                                out_data = json.dumps(output, indent=2, ensure_ascii=False)
                                f.write(out_data)


                            item_count = item_count + 1
                            not_matched = ''
                            record_line_num = 0
                        break                              #found a match so break out of loop and go to next word

                if(matched == False):
                    #print "NOT MATCHED: " + line
                    not_matched = not_matched + "\n" + line  #load all of these non-matching lines into one field so we can analyze
                    

            record_line_num += 1
            #print record_line_num





def match_with_word(word, line):
    word_length = len(word[0])            #check the length of the word

    if line.split(":")[0].lower() == word[0].lower():   
        #we've got a match!
        #grab the contents to the right
        #print "label: " + word[0]
        #label_text = line.split(":")[0] + ':'
        #print line.replace(label_text,"",1).strip() + '\n'  #print the matching line without the label
        return True
    else:
        return False



def to_open_referral(entry):

    # Default values.


    city, state, zip, = '', '', ''
    #languages = entry.languages_spoken
    #short_description = entry.services_provided[:100]
    #name, title = entry.contact, ''

    # Apply fanciness.

    # if ', San Francisco' in entry.address:
    #     entry.address = entry.address.replace(', San Francisco', '')
    #     city = 'San Francisco'
    # if ', CA' in entry.address:
    #     entry.address = entry.address.replace(', CA', '')
    #     state = 'CA'
    # zip_regex = '( [0-9]{5})$'
    # match = re.search(zip_regex, entry.address)
    # if match:
    #     zip = match.group(0).strip()
    #     entry.address = re.sub(zip_regex, '', entry.address)
    # languages = languages.replace(' and ', '').split(', ')
    # if ',' in name:
    #     name, title = [s.strip() for s in name.rsplit(',', 1)]

    # short_description = sent_detector.tokenize(
    #     entry.services_provided.strip())[0]

    # Fill in the blanks.

    return {
        'name':entry.organization_name,
        'locations':[
            {
                'name':entry.organization_name,  
                'contacts_attributes':[  
                    {
                        'name':'none',  
                        'title':'none',  
                    }
                ],
                'description':'none',
                'short_description':'none',
                'address_attributes':{
                    'street':'none' ,
                    'city':'none' ,
                    'state':'none' ,
                    'zip':'none' 
                },
                "mail_address_attributes": {
                    "attention": entry.organization_name,
                    "street": 'none',
                    "city": 'none',
                    "state":'none' ,
                    "zip": 'none'
                },
                "hours":'none' ,
                "transportation": "none",
                "accessibility": [
                ],
                "languages":'none',
                "emails": [
                    'none'
                ],
                "faxes_attributes": [
                    {
                        "number": 'none'
                    }
                ],
                "phones_attributes": [
                    {
                        "number": 'none'
                    }
                ],
                "urls": [
                    'none'
                ],
                "services_attributes": [
                    {
                        "audience": "none",
                        "eligibility": entry.eligibility,
                        "fees": entry.fees,
                        "how_to_apply": "",
                        "service_areas": [],
                        "keywords": [entry.keywords],
                        "wait": "",
                        "funding_sources": []
                    }
                ],
            }
        ],
    }






if __name__ == '__main__':
    scraper(open(argv[1]))


