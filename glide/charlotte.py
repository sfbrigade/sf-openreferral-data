import re
import os
import itertools

import requests

class Webpage:
  def __init__(self, url):

    # Create cache if necessary.  Load cached html if it exists.

    self.url = url
    normal_url = url.replace('/', '-').replace(':', '-')
    cache_root =  os.path.expanduser(os.path.join('~', 'charlotte_cache'))
    if not os.path.exists(cache_root):
      os.mkdir(cache_root)
    self.cache_path = os.path.join(cache_root, normal_url)
    if os.path.exists(self.cache_path):
      with open(self.cache_path) as f:
        self.html = f.read()
    else:
      self.download()
    self.parse_html()

  def download(self):

    # Request the page, download the html to the cache.

    self.html = requests.get('http://www.glide.org/').content
    with open(self.cache_path, 'w') as f:
      f.write(self.html)

  def parse_html(self):

    # Pull interesting info out of html.

    html = self.html
    self.link_urls = re.findall('<a.+?href="(.+?)">.+?</a>', html)
    address_regex = '[0-9]+ .+?, San Francisco, CA [0-9]+'
    self.address = re.search(address_regex, html).group()

  def spider(self):
    for i, url in enumerate(self.link_urls[:10]):
      print 'hitting link {}/{}'.format(i + 1, len(self.link_urls))
      hit_url(url)

the_internet = {}

def hit_url(url):
  the_internet[url] = page = Webpage(url)
  return page

if __name__ == '__main__':
  page = hit_url('http://www.glide.org/')
  page.spider()
  all_links = list(itertools.chain(
    *[page.link_urls for page in the_internet.values()]))
  all_addresses = [page.address for page in the_internet.values()]
  print 'num links found:', len(all_links)
  print 'addresses:', len(all_addresses)
  for addr in all_addresses:
    print addr

