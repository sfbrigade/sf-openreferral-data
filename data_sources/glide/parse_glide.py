
import re

from nltk.tag import pos_tag

def find_phone_numbers():
  with open('glide_contact_page.txt') as f:
    contact_text = f.read()
  no_tags = re.sub('<.*?>', ' ', contact_text)
  words = [word.strip() for word in re.split('\s+', no_tags)]
  for word in words:
    if re.search('[0-9]{3}.[0-9]{3}.[0-9]{4}', word):
      yield word

def find_name():
  with open('glide.txt') as f:
    front_text = f.read()

  no_tags = re.sub('<.*?>', '', front_text)
  no_tags = [word.strip().lower() for word in no_tags.split(' ') if word]

  word_counts = {}
  for word in no_tags:
    word_counts.setdefault(word, 0)
    word_counts[word] += 1
  for word, count in sorted(
    word_counts.iteritems(), key=lambda x: -x[1])[:20]:
    if len(word) > 3:
      return word

def find_addresses():
  with open('glide_contact_page.txt') as f:
    contact_text = f.read()
  no_tags = re.sub('<.*?>', ' ', contact_text)
  return re.findall('[0-9]+ [a-zA-Z]+ Street', no_tags)

print 'name:', find_name()
print 'phone numbers:', list(find_phone_numbers())
print 'addresses:', find_addresses()


# print 'tagging'
# tagged_sent = pos_tag(words[:100])
# print 'tagged'

# propernouns = [word for word,pos in tagged_sent if pos == 'NNP']
# print propernouns
# # ['Michael','Jackson', 'McDonalds']