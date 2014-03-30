from sys import argv
from re import match

def print_the_thing(org_name, addresses):
    if org_name != '' and addresses != []:
        for address in addresses:
            print '"' + org_name + '", "' + address + '"'

def scraper(file):
    imp_words = [
            ['Organization Name', ""],
            ['Address', ""],
            ['Phone', ""],
            ['Fax', ""],
            ['Email', ""],
            ['Website', ""],
            ['Contact', ""],
            ['Age Groups', ""],
            ['Languages Spoken', ""],
            ['Fees', ""],
            ['Service Hours', ""],
            ['Services Provided', ""],
            ]
    print ', '.join(['"%s"' % x[0] for x in imp_words])
# Operating under the assumption that services and name are required
    current_word = None
    previous_word = None
    total_words = len(imp_words)
    bit = 0
    for i, line in enumerate(file):
        line = line.strip()
        bit = 0
        for count, word in enumerate(imp_words):
            word_length = len(word[0])
            if line[:word_length] == word[0]:
                if previous_word and count == 0:
                    for address in imp_words[1][1:]:
                        print '"%s", "%s", ' % (imp_words[0][1], address),
                        print ', '.join(['"%s"' % x[1] for x in imp_words[2:]])
                    imp_words[1] = ['Address', ""]
                previous_word = current_word
                word[1] = line[word_length:].strip()
                current_word = count
                bit = 1
                break
            else:
                continue

        if bit == 0 and current_word and line and not match('^\d{1,3}$',line):
            if current_word == 1:
                imp_words[current_word].append(line)
            else:
                imp_words[current_word][1] += " "
                imp_words[current_word][1] += line

    for address in imp_words[1][1:]:
        print '"%s", "%s", ' % (imp_words[0][1], address),
        print ', '.join(['"%s"' % x[1] for x in imp_words[2:]])

if __name__ == '__main__':
    scraper(open(argv[1]))

