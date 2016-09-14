
import os
import sys
import re
import time
from urllib import urlopen
from bs4 import BeautifulSoup
base_url = "http://projects.nytimes.com"
index_ref  = "/guatanamo/detainees/current"
index_html = urlopen(base_url + index_ref)
# Parsed version of html - that is what a BeautifulSoup object is.
index = BeautifulSoup(index_html, 'lxml')
# Allows us to visualize how we might distinguish the links we care about
# from those we don't
print index.prettify()
# Look at the elements of the HTML - where the css style sheets are etc.
index.head
# Now look at the body - this is where the links are
index.body
# You might take note of the renderings class of the links you want, because
# you may be able to just grab all the links that have that style class as
# a proxy!

# Find the patterns for the types of content you want. (Regex type stuff)
# re.compile(pattern)
# \d match digits
# \w match words (alphanumerics)
# Many more at https://docs.python.org/3/library/re.html
# Note, for example that the links of interest follow this pattern:
#     .../detainees/##
prisoner_links = index.find_all('div', {'class': 'nyint-detainee-fullcol'})
print len(prisoner_links)
# print prisoner_links
# Define a function wrapper for grabbing
def try_request(url):
    html = urlopen(url)
    time.sleep(5)
    return html

def scrape_link(links):
    for link in links:
        # Turn the link into an html file
        prisoner_html = try_request(base_url + index_ref)
        name = test.find('h1').get_text().strip()
        country = test.find('a', href=re.compile('/country/')).get_text()
        time_in_gitmo= test.find(text=re.compile('for \d+ years')).lstrip('for ').strip().rsplit('.\n\n',1)[0]
        return {'name': name, 'country': country, 'time':time_in_gitmo}
        # go to the link
        # save the stuff we care about
prisoners = {}
link_num = 0
for link in prisoner_links:
    link_num += 1
    print link_num
    # prisoners[link_num] = scrape_link[link]
print prisoners
