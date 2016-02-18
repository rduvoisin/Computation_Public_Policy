# Rebeccah Duvoisin
# Assignment 4
import os
import sys
import re
import time
from urllib import urlopen
from bs4 import BeautifulSoup
'''
Web Scraping

You’ll be scraping data from this website,
which contains a list of incidents involving
commercial aircraft listed by year.

Part a
Write a scraper that will produce a pandas dataframe containing the following columns:

    When the accident occurred (year, month, and day - use a datetime object)
    The short text description (everything to the right of the date)
    The link to the detail page.
'''
base_url = "https://en.wikipedia.org"
index_ref  = "/wiki/List_of_accidents_and_incidents_involving_commercial_aircraft"
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
index.body.prettify()
# You might take note of the renderings class of the links you want, because
# you may be able to just grab all the links that have that style class as
# a proxy!
# Pattern = href="/wiki/1933_United_Airlines_Boeing_247_mid-air_explosion" title="
# /wiki/

# Find the patterns for the types of content you want. (Regex type stuff)
# re.compile(pattern)
# \d match digits
# \w match words (alphanumerics)
# Many more at https://docs.python.org/3/library/re.html
# Note, for example that the links of interest follow this pattern:
#     .../detainees/##
wiki_links = index.find_all('a', href=re.compile('^/wiki/'))
# pattern =
for wiki_link in wiki_links:
    print wiki_link['href']
print len(wiki_links)
# <li>August 2 – A <b><a href="/wiki/1919_Verona_Caproni_Ca.48_crash"
# title="1919 Verona Caproni Ca.48 crash">Caproni Ca.48 crashes at Verona</a></b>,
# Italy, during a flight from Venice to Taliedo, Milan, killing all on board
# (14, 15, or 17 people, according to different sources).</li>
#
# <h3><span class="mw-headline" id="1919">1919</span><span class="mw-editsection"><span class="mw-editsection-bracket">[</span><a href="/w/index.php?title=List_of_accidents_and_incidents_involving_commercial_aircraft&amp;action=edit&amp;section=2" title="Edit section: 1919">edit</a><span class="mw-editsection-bracket">]</span></span></h3>
# <ul>
# <li>August 2 – A <b><a href="/wiki/1919_Verona_Caproni_Ca.48_crash" title="1919 Verona Caproni Ca.48 crash">Caproni Ca.48 crashes at Verona</a></b>, Italy, during a flight from Venice to Taliedo, Milan, killing all on board (14, 15, or 17 people, according to different sources).</li>
# </ul>
# <h3><span class="mw-headline" id="1922">1922</span><span class="mw-editsection"><span class="mw-editsection-bracket">[</span><a href="/w/index.php?title=List_of_accidents_and_incidents_involving_commercial_aircraft&amp;action=edit&amp;section=3" title="Edit section: 1922">edit</a><span class="mw-editsection-bracket">]</span></span></h3>
# <ul>
# <li>April 7 – In the <b><a class="mw-redirect" href="/wiki/First_mid-air_collision_of_airliners" title="First mid-air collision of airliners">first mid-air collision of airliners</a></b>, a de Havilland DH.18A, <i>G-EAWO</i>, operated by Daimler Hire Ltd., collides with a Farman F.60 Goliath, <i>F-GEAD</i>, operated by Compagnie des Grands Express Aériens (CGEA), over the Thieulloy-St. Antoine road near Picardie, France, killing all seven people on both aircraft.</li>
# </ul>
# <h3><span class="mw-headline" id="1923">1923</span><span class="mw-editsection"><span class="mw-editsection-bracket">[</span><a href="/w/index.php?title=List_of_accidents_and_incidents_involving_commercial_aircraft&amp;action=edit&amp;section=4" title="Edit section: 1923">edit</a><span class="mw-editsection-bracket">]</span></span></h3>
# <ul>
# <li>May 14 – An <b><a href="/wiki/May_1923_Air_Union_Farman_Goliath_crash" title="May 1923 Air Union Farman Goliath crash">Air Union Farman F.60 Goliath crashes</a></b> near Monsures, Somme, France, due to the structural failure of a wing, killing all 6 on board.</li>
# <li>August 27 – An <b><a href="/wiki/August_1923_Air_Union_Farman_Goliath_crash" title="August 1923 Air Union Farman Goliath crash">Air Union Farman F.60 Goliath crashes</a></b> near East Malling, Kent, England, due to engine failure, and confusion among the passengers, killing one of 13 on board.</li>
# </ul>
# <h3><span class="mw-headline" id="1924">1924</span><span class="mw-editsection"><span class="mw-editsection-bracket">[</span><a href="/w/index.php?title=List_of_accidents_and_incidents_involving_commercial_aircraft&amp;action=edit&amp;section=5" title="Edit section: 1924">edit</a><span class="mw-editsection-bracket">]</span></span></h3>
first_header3 = index.find('h3')
all_headers = index.find_all('h3')
header_lists_dic = {}
header_lists_year_dics = {}
# def get_crash_dict_links(all_header3):
header_lists_year_dics = {}
def new_bullet_from_li(header_li, header_lists_year_dics=header_lists_year_dics,
                       year=None, header_date=None, header_brief=None):
    is_a = header_li
    while is_a.name != 'a':
        is_a = is_a.next_element
    print 'is_a!', is_a.name, is_a.contents
    header_href = is_a.get('href')
    header_bullet = {'year': year, 'date': None, 'link': None, 'brief': None, 'place':None}
    header_bullet['date'] = header_date
    header_bullet['link'] = header_href
    header_bullet['brief'] = header_brief
    print 'header_bullet = {}'.format(header_bullet)
    header_dict = {}
    header_dict[header_bullet['link']] = header_bullet
    print 'header_dict', header_dict
    empty_list = []
    header_lists_year_dics[year] = \
        header_lists_year_dics.get(year, {})
    if isinstance(header_date, list):
        for each_date in header_date:
            header_lists_year_dics[year][each_date] = \
                header_lists_year_dics[year].get(each_date, [])
            print 'header_lists_year_dics[year][each_date]', header_lists_year_dics[year][each_date]
            if header_lists_year_dics[year][each_date]:
                header_lists_year_dics[year][each_date].append(header_dict)
            else:
                header_lists_year_dics[year][each_date] = [header_dict]
    else:
        header_lists_year_dics[year][header_date] = \
            header_lists_year_dics[year].get(header_date, [])
        print 'header_lists_year_dics[year][header_date]', header_lists_year_dics[year][header_date]
        if header_lists_year_dics[year][header_date]:
            header_lists_year_dics[year][header_date].append(header_dict)
        else:
            header_lists_year_dics[year][header_date] = [header_dict]

for i in range(len(all_header3)):
    print "TWEET {}\n".format(i)
    print all_header3[i]
    this_header = all_header3[i]
    this_header.next_sibling.next_sibling
    is_911 = False
    # if not this_header.span:
    #     return header_lists_year_dics
    year = this_header.span.get('id')
    is_ul = this_header
    while is_ul.name != 'ul':
        is_ul = is_ul.next_sibling
    print 'is_ul!', is_ul.name, is_ul.contents
    print len(is_ul.contents)
    listings = [is_ul.contents[i] for i in range(len(is_ul.contents[:-1])) if i%2>0]
    print 'listings', listings
    for listing in listings:
        header_li = listing
        print 'header_li = {}'.format(header_li)
        if len(header_li.findChildren('li')) > 0:
            header_date = []
            header_brief = []
            for subbullet_li in header_li.findChildren('li'):
                if not subbullet_li.next_element.name:
                    strip_date = subbullet_li.next_element[:-2].strip()
                else:
                    strip_date = header_li.next_element[:-2].strip()
                    is_911 = True
                # Add description too
                # if sub_date.strip() == "Septemeber 11":
                #     header_date = sub_date
                # else:
                print 'strip_date', strip_date
                sub_dater = re.match('(^\w+ \w+)(.*)', strip_date)
                print 'sub_dater', sub_dater
                sub_date = sub_dater.group(1)
                print 'sub_date', sub_date
                # strip text
                if not subbullet_li.next_element.name:
                    header_date.append(sub_date)
                    sub_text = sub_dater.group(2).strip()
                    header_brief.append(re.search('(\w+)(.*)', sub_text).group(0))
                else:
                    header_brief = subbullet_li.contents[-1]
                    new_bullet_from_li(subbullet_li, header_lists_year_dics, year, sub_date, header_brief)
        else:
            header_brief = None
            strip_date = header_li.next_element[:-2].strip()
            print 'strip_date', strip_date
            header_dater = re.match('(^\w+ \w+)', strip_date)
            print 'header_dater', header_dater
            header_date = header_dater.group(0)
            print 'header_date', header_date
        if not is_911:
            is_a = header_li
            while is_a.name != 'a':
                is_a = is_a.next_element
            print 'is_a!', is_a.name, is_a.contents
            header_href = is_a.get('href')
            header_bullet = {'year': year, 'date': None, 'link': None, 'brief': None, 'place':None}
            header_bullet['date'] = header_date
            header_bullet['link'] = header_href
            header_bullet['brief'] = header_brief
            print 'header_bullet = {}'.format(header_bullet)
            header_dict = {}
            header_dict[header_bullet['link']] = header_bullet
            print 'header_dict', header_dict
            empty_list = []
            header_lists_year_dics[year] = \
                header_lists_year_dics.get(year, {})
            # print 'header_lists_year_dics', header_lists_year_dics
            if isinstance(header_date, list):
                for each_date in header_date:
                    header_lists_year_dics[year][each_date] = \
                        header_lists_year_dics[year].get(each_date, [])
                    print 'header_lists_year_dics[year][each_date]', header_lists_year_dics[year][each_date]
                    if header_lists_year_dics[year][each_date]:
                        header_lists_year_dics[year][each_date].append(header_dict)
                    else:
                        header_lists_year_dics[year][each_date] = [header_dict]
            else:
                header_lists_year_dics[year][header_date] = \
                    header_lists_year_dics[year].get(header_date, [])
                print 'header_lists_year_dics[year][header_date]', header_lists_year_dics[year][header_date]
                if header_lists_year_dics[year][header_date]:
                    header_lists_year_dics[year][header_date].append(header_dict)
                else:
                    header_lists_year_dics[year][header_date] = [header_dict]
            # header_lists_year_dics[year][header_bullet['link']] = header_bullet
        print 'header_lists_year_dics', header_lists_year_dics
        # return header_lists_year_dics

print 'header_lists_year_dics', header_lists_year_dics

    for sister in all_header3[i].findNextSiblings():
        if sister.name == 'h3':
            break
        if sister.name == 'li':

    print all_header3[i].next_element  # next_sibling, descendents, children


month = re.match(r'(^\w [1-31])', first_header3.next_sibling.next_sibling.contents[1])
hlist = fh.next_sibling.next_sibling.contents[1]
month = re.match('(^<li>)(\w [1-31])', fh.next_sibling.next_sibling.contents[1])

first_list = index.find_all('li') .find_all()'a',  href=re.compile('^/wiki/'))
wiki_lists = index.find_all('li', text="^[A-Z][a-z]+ - ", href=re.compile('^/wiki/'))
wiki_lists = index.find_all('li')
# pattern =
for wiki_list in wiki_lists:
    print wiki_list['href']

table_cards = index.find_all('table', {'class': 'infobox vcard vevent'})
# pattern =
for card in table_cards:
    print card['TEXT']

crashes_links = index.find_all('div', {'class': 'nyint-detainee-fullcol'})
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
