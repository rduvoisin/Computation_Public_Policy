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
class Crash(object):
    '''
    Initiates a class to hold attributes of a scraped Wiki crash;
    - *link
    - *li object
    - *year
    - *date
    - *brief
    - place
    - crew
    - passengers
    - fatalities
    - survivors
    - registration
    - origin
    - destination
    '''

    def __init__(self, key, dictionary, li_object=None):

        self.__link = dictionary['link']
        self.__li = li_object
        self.year = dictionary['year']  # Public; mutable anytime.
        self.date = dictionary['date']  # Public; mutable anytime.
        self.brief = dictionary['brief']  # Public; mutable anytime.
        self.place = None
        self.crew = None
        self.passengers = None
        self.fatalities = None
        self.survivors = None
        self.registration = None
        self.origin = None
        self.destination = None

    @property
    def link(self):
        return self.__link

    @property
    def li(self):
        return self.__li

    @property
    def year(self):
        return self.year

    @property
    def date(self):
        return self.date

    @property
    def brief(self):
        return self.brief

    @property
    def place(self):
        return self.place


def parse_crashes_to_dict(all_header3):
    '''
    Input: a group of h3 headers that contain hierarchical html lists.
    Returns: A dictionary of years to dictionaries of dates and link
        information:
        -date: the date of the crash.
        -link: the link to further info on the crash.
        -brief: a brief description of the accident.
        -place: the location of the crash.
    '''
    header_lists_year_dics = {}
    for i in range(len(all_header3)):
        print "TWEET {}\n".format(i)
        print all_header3[i]
        this_header = all_header3[i]
        this_header.next_sibling.next_sibling
        is_911 = False
        if not this_header.span:
            print "\nOp! All Done!"
            return header_lists_year_dics
        year = int(this_header.span.get('id'))
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
                    has_same_date = False
                    if not subbullet_li.next_element.name:
                        is_date = re.match('([1-9]+)', subbullet_li.next_element.split()[1])
                        if is_date:
                            strip_date = subbullet_li.next_element[:-2].strip()
                        else:
                            strip_date = header_li.next_element[:-2].strip()
                            has_same_date = True
                    else:
                        strip_date = header_li.next_element[:-2].strip()
                        is_911 = True
                        has_same_date = True
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
                        if has_same_date:
                            header_brief = subbullet_li.contents[-1]
                        else:
                            sub_text = sub_dater.group(2).strip()
                            header_brief.append(re.search('(\w+)(.*)', sub_text).group(0))
                    else:
                        header_brief = subbullet_li.contents[-1]
                        new_bullet_from_li(subbullet_li, header_lists_year_dics, year, sub_date, header_brief)
            else:
                header_brief = header_li.text
                strip_date = header_li.next_element[:-2].strip()
                print 'strip_date', strip_date
                header_dater = re.match('(^\w+ \w+)', strip_date)
                print 'header_dater', header_dater
                header_date = header_dater.group(0)
                print 'header_date', header_date
            if not is_911:
                new_bullet_from_li(header_li, header_lists_year_dics, year, header_date, header_brief)
            #     is_a = header_li
            #     while is_a.name != 'a':
            #         is_a = is_a.next_element
            #     print 'is_a!', is_a.name, is_a.contents
            #     header_href = is_a.get('href')
            #     header_bullet = {'year': year, 'date': None, 'link': None, 'brief': None, 'place':None}
            #     header_bullet['date'] = header_date
            #     header_bullet['link'] = header_href
            #     header_bullet['brief'] = header_brief
            #     print 'header_bullet = {}'.format(header_bullet)
            #     header_dict = {}
            #     header_dict[header_bullet['link']] = header_bullet
            #     print 'header_dict', header_dict
            #     empty_list = []
            #     header_lists_year_dics[year] = \
            #         header_lists_year_dics.get(year, {})
            #     # print 'header_lists_year_dics', header_lists_year_dics
            #     if isinstance(header_date, list):
            #         for each_date in header_date:
            #             header_lists_year_dics[year][each_date] = \
            #                 header_lists_year_dics[year].get(each_date, [])
            #             print 'header_lists_year_dics[year][each_date]', header_lists_year_dics[year][each_date]
            #             if header_lists_year_dics[year][each_date]:
            #                 header_lists_year_dics[year][each_date].append(header_dict)
            #             else:
            #                 header_lists_year_dics[year][each_date] = [header_dict]
            #     else:
            #         header_lists_year_dics[year][header_date] = \
            #             header_lists_year_dics[year].get(header_date, [])
            #         print 'header_lists_year_dics[year][header_date]', header_lists_year_dics[year][header_date]
            #         if header_lists_year_dics[year][header_date]:
            #             header_lists_year_dics[year][header_date].append(header_dict)
            #         else:
            #             header_lists_year_dics[year][header_date] = [header_dict]
            #     header_lists_year_dics[year][header_bullet['link']] = header_bullet
            # print 'header_lists_year_dics', header_lists_year_dics
            # # return header_lists_year_dics
    return header_lists_year_dics

def new_bullet_from_li(header_li, header_lists_year_dics=header_lists_year_dics,
                       year=None, header_date=None, header_brief=None):
    '''
    Helper function for parse_crashes_to_dict.

    Inputs: One html 'li' list, and other information
    pertaining to it.

    Returns: A dictionary of years to dictionaries for the li.
        -date: the date of the crash.
        -link: the link to further info on the crash.
        -brief: a brief description of the accident.
        -place: the location of the crash.
    '''
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

crash_dict = parse_crashes_to_dict(all_headers)

# wiki_lists = index.find_all('li')
for wiki_list in wiki_lists:
    print wiki_list['href']
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
