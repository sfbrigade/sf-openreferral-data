from sys import argv
from re import match

def scraper(file):
    imp_words = [
            ['Administration Mailing Address', ""],
            ['Administrative Office', ""],
            ['Office location', ""],
            ['Intake location', ""],
            ['Mailing Address', ""],
            ['Main Office', ""],
            ['Corporate Office', ""],
            ['24-Hour Hotline', ""],
            ['Toll-Free Telephone', ""],
            ['General Inquiries', ""],          
            ['Emergency Center Phone', ""],
            ['Emergency Bed Call-in #', ""],
            ['Address', ""],
            ['Primary Community Served', ""],
            ['Notes', ""],
            ['Info Line', ""],
            ['Phone', ""],
            ['Main Phone', ""],
            ['Intake Phone', ""],
            ['Hours', ""],
            ['Clinic Hours', ""],
            ['Hours/Meeting times', ""],
            ['Intake Hours', ""],
            ['Drop-in Hours', ""],
            ['Program Hours', ""],
            ['Specific Intake Days and Times', ""],
            ['Days and Hours', ""],
            ['TDD', ""],
            ['Fax', ""],
            ['Email', ""],
            ['E-mail', ""],
            ['url', ""],
            ['Languages Spoken', ""],
            ['What to Bring', ""],
            ['Things to Know', ""],
            ['Accessibility', ""],
            ['Client fees, if any', ""],
            ['Client fee, if any', ""],
            ['Client fee\'s, if any', ""],
            ['Client fees', ""],
            ['Eligible Population', ""],
            ['Eligible Populations', ""],
            ['Eligible Population Served', ""],
            ['Not Eligible', ""],
            ['Restrictions', ""],
            ['Direct Services', ""],
            ['Direct Service', ""],
            ['Faith Based', ""],
            ['Contact Persons', ""],
            ['Contact Person', ""],
            ['Contact', ""],
            ['Person to Contact', ""],
            ['Intake Days', ""],
            ['Facility Hours', ""],
            ['Drop-In Clinic Hours', ""],
            ['Location', ""],
            ['Locations', ""],
            ['Services', ""],
            ['Days and Times', ""],
            ['Note', ""],
            ]
    line_count = 0
    not_matched = ''
    record_line_num = 1
    total_words = len(imp_words)
    for i, line in enumerate(file):   #go line by line
        line = line.strip()           #pull out extra spacing

        if (len(line) > 0) and (line.find('Things To Know')) and (line.find('To Get Connected')):  #skip if it's a blank line or contains a known header
            if record_line_num == 1:     #we're at the first line of the file or the first line of a new record, must be the title
                print "\nBOR -----------------------------------------------------------------\n"
                print "Title: " + line + "\n"
            elif record_line_num == 2:   #second line is the description...hopefully
                print "Description: " + line + "\n"
                print ""
            else:
                matched = False
                
                for count, word in enumerate(imp_words):  #loop through every important word and look for a match on this line  

                    matched = match_with_word(word, line) #test for a match between word and line
                    if(matched):                          #we've got a match
                        if word[0].lower() == "direct services":  #are we at the end of the record?
                            print "NOT MATCHED THIS RECORD: " + not_matched    #if so, print the list of non matching data so we can deal with later
                            print "\nEOR -----------------------------------------------------------------\n"
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
        print "label: " + word[0]
        label_text = line.split(":")[0] + ':'
        print line.replace(label_text,"",1).strip() + '\n'  #print the matching line without the label
        return True
    else:
        return False


if __name__ == '__main__':
    scraper(open(argv[1]))

