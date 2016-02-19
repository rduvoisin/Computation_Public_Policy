# Rebeccah Duvoisin
# Assignment 4
import os
import sys
import re
import time
from urllib import urlopen
from bs4 import BeautifulSoup
import pandas as pd
'''
Web Scraping

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
# print index.prettify()
# Look at the elements of the HTML - where the css style sheets are etc.
# index.head
# Now look at the body - this is where the links are
# index.body
# index.body.prettify()
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
# wiki_links = index.find_all('a', href=re.compile('^/wiki/'))
# # pattern =
# for wiki_link in wiki_links:
#     print wiki_link['href']
# print len(wiki_links)


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

    def __init__(self, dictionary, li_object=None):
        self.__link = dictionary['link']
        self.__li = li_object
        self._year = dictionary['year']  # Public; mutable anytime.
        self._date = dictionary['date']  # Public; mutable anytime.
        self._brief = dictionary['brief']  # Public; mutable anytime.
        self._place = None
        self._crew = None
        self._passengers = None
        self._fatalities = None
        self._survivors = None
        self._registration = None
        self._origin = None
        self._destination = None


    @property
    def link(self):
        return self.__link

    @property
    def li(self):
        return self.__li

    @property
    def year(self):
        return self._year

    @property
    def date(self):
        return self._date

    @property
    def brief(self):
        return self._brief

    @property
    def place(self):
        return self._place

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
        listings = [is_ul.contents[i] for i in range(len(is_ul.contents[:-1])) if i%2>0]
        for listing in listings:
            header_li = listing
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
                    sub_dater = re.match('(^\w+ \w+)(.*)', strip_date)
                    sub_date = sub_dater.group(1)
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
                strip_date = header_li.next_element[:-2].strip()
                header_dater = re.match('(^\w+ \w+)(.*)', strip_date)
                header_date = header_dater.group(1)
                header_text = header_li.get_text()
                header_brief = re.sub(strip_date, '', header_text, 1).strip()
            if not is_911:
                new_bullet_from_li(header_li, header_lists_year_dics, year, header_date, header_brief)
    return header_lists_year_dics

def new_bullet_from_li(header_li, header_lists_year_dics=dict,
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
    header_href = is_a.get('href')
    header_bullet = {'year': year, 'date': None, 'link': None, 'brief': None, 'place':None}
    header_bullet['date'] = header_date
    header_bullet['link'] = header_href
    header_bullet['brief'] = header_brief
    header_dict = Crash(header_bullet, header_li)
    empty_list = []
    header_lists_year_dics[year] = \
        header_lists_year_dics.get(year, {})
    if isinstance(header_date, list):
        for each_date in header_date:
            header_lists_year_dics[year][each_date] = \
                header_lists_year_dics[year].get(each_date, empty_list)
            if header_lists_year_dics[year][each_date]:
                header_lists_year_dics[year][each_date].append(header_dict)
            else:
                header_lists_year_dics[year][each_date] = [header_dict]
    else:
        header_lists_year_dics[year][header_date] = \
            header_lists_year_dics[year].get(header_date, empty_list)
        if header_lists_year_dics[year][header_date]:
            header_lists_year_dics[year][header_date].append(header_dict)
        else:
            header_lists_year_dics[year][header_date] = [header_dict]

def dict_todataframe(crash_dict):
    '''
    Helper function for transforming dictionary into matrix.
    Inputs: One crash dictionary of {years:dates:[crash_objects]}
    Returns: A pandas DataFrame.
    '''
    month_dict = {1: 'January', 2:'February', 3:'March', 4:'April',
                  5:'May', 6: 'June', 7: 'July', 8: 'August', 9:'September',
                  10: 'October', 11:'November', 12:'December'}

    dict_month = {}
    for k in month_dict.keys():
        dict_month[month_dict[k]] = k
    dates = []
    events = []
    for year in crash_dict.keys():
        string_dates = []
        crash_objects = []
        for date in crash_dict[year].keys():
            month = dict_month[str(date.split()[0])]
            day = int(str(date.split()[1]))
            crash_date = str(year) + str(month).zfill(2) + str(day).zfill(2)
            for c_ob in range(len(crash_dict[year][date])):
                string_dates.append(crash_date)
                crash_objects.append(crash_dict[year][date][c_ob])
        dates.extend(string_dates)
        events.extend(crash_objects)
        print {'Dates': string_dates, 'Crash': crash_objects}
    print '\nFinished:'
    print {'Dates': len(dates), 'Crash': len(events)}
    return pd.DataFrame({'Date':dates, 'Crash': events})

all_headers = index.find_all('h3')
crash_dict = parse_crashes_to_dict(all_headers)


crashes = dict_todataframe(crash_dict)
date = 'Date'
crashes[date] = pd.to_datetime(crashes[date])
crash = 'Crash'
var_list = ['link', 'brief']
# for variable in var_list:
#     print variable
#     crashes[variable] = crashes[crash].apply(lambda c: c.variable)
crashes['Link'] = crashes[crash].apply(lambda c: c.link)
crashes['Brief'] = crashes[crash].apply(lambda c: c.brief)
# # wiki_lists = index.find_all('li')
# for wiki_list in wiki_lists:
#     print wiki_list['href']
# # Define a function wrapper for grabbing
# def try_request(url):
#     html = urlopen(url)
#     time.sleep(5)
#     return html
#
# def scrape_link(links):
#     for link in links:
#         # Turn the link into an html file
#         prisoner_html = try_request(base_url + index_ref)
#         name = test.find('h1').get_text().strip()
#         country = test.find('a', href=re.compile('/country/')).get_text()
#         time_in_gitmo= test.find(text=re.compile('for \d+ years')).lstrip('for ').strip().rsplit('.\n\n',1)[0]
#         return {'name': name, 'country': country, 'time':time_in_gitmo}
#         # go to the link
#         # save the stuff we care about
# prisoners = {}
# link_num = 0
# for link in prisoner_links:
#     link_num += 1
#     print link_num
#     # prisoners[link_num] = scrape_link[link]
# print prisoners
