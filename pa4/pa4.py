# Rebeccah Duvoisin
# Assignment 4
import os
import sys
import re
import time
from urllib import urlopen
from bs4 import BeautifulSoup
import requests
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

    @place.setter
    def place(self, place_string):
        self._place = place_string

    @property
    def crew(self):
        return self._crew

    @crew.setter
    def crew(self, crew_string):
        self._crew = crew_string

    @property
    def passengers(self):
        return self._passengers

    @passengers.setter
    def passengers(self, passengers_string):
        self._passengers = passengers_string

    @property
    def fatalities(self):
        return self._fatalities

    @fatalities.setter
    def fatalities(self, fatalities_string):
        self._fatalities = fatalities_string

    @property
    def survivors(self):
        return self._survivors

    @survivors.setter
    def survivors(self, survivors_string):
        self._survivors = survivors_string

    @property
    def registration(self):
        return self._registration

    @registration.setter
    def registration(self, registration_string):
        self._registration = registration_string

    @property
    def origin(self):
        return self._origin

    @origin.setter
    def origin(self, origin_string):
        self._origin = origin_string

    @property
    def destination(self):
        return self._destination

    @destination.setter
    def destination(self, destination_string):
        self._destination = destination_string

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
    return pd.DataFrame({'Date':dates, 'Crash': events})

def make_dataframe(pattern='h3', DATE='Date', CRASH='Crash', LINK='Link', BRIEF='Brief'):
    print 'QUESTION 1: Part A\n Parsing data into dictionary...'
    all_headers = index.find_all(pattern)
    crash_dict = parse_crashes_to_dict(all_headers)
    print '\nBuilding dataframe from dictionary...'
    crashes = dict_todataframe(crash_dict)
    crashes[DATE] = pd.to_datetime(crashes[DATE])
    crashes[LINK] = crashes[CRASH].apply(lambda c: c.link)
    crashes[BRIEF] = crashes[CRASH].apply(lambda c: c.brief)
    print '\nDataframe built:\n Shape:', \
            crashes.shape, '\n Columns:', \
            crashes.columns, '\n Head 50:\n', \
            crashes.head(50)
    return crashes
'''
Part b

Now write a code that clicks each link and scrapes additional
content from the detailed page associated with each individual
crash.
How will you ensure that you rate limit your requests
to the target web server?
Once you have implemented this feature,
scrape the content located in the right column of each
details page and add it to the pandas dataframe:

    Number of passengers
    Number of crew
    Number of fatalities
    Number of survivors
    Registration
    Flight origin
    Destination
'''
def grab_link_like_person(url):
    # html = urlopen(url)
    source_code = requests.get(url)
    time.sleep(5)
    return source_code

def scrape_link(crash_links):
    for crash_link in crash_links:
        # Turn the link into an html file
        print "\n", crash_link.date
        print crash_link.brief
        print crash_link.link
        print base_url + crash_link.link
        link_html = grab_link_like_person(base_url + crash_link.link)
        # crash_html = BeautifulSoup(link_html, 'lxml')
        crash_html = BeautifulSoup(link_html.text, 'lxml')
        table_rows = crash_html.find('table').find_all('tr')
        data = []
        for row in table_rows[2:]:
            # print row
            new_tuple = row.get_text().strip().split('\n')
            # print new_tuple
            # key = new_tuple[0]
            # value = new_tuple[1]
            # if key =='Date':
            #     new_value = re.findall(r'(\d+)\-(\d+)\-(\d+)', value)
            #     new_date =  new_value[0][0] + new_value[0][1] + new_value[0][2]
            #     new_tuple[1] = new_date
            if new_tuple[0] =='Site':
                new_tuple.pop()
            # new_tuple[1] = re.sub(r'(\[\d+\])','', new_tuple[1])
            data.append(new_tuple)
        paired_data = [[element[0], element[1]] for element in data if len(element) > 1]
        # print 'DATA'
        # for element in data:
        #     print element
        # print 'PAIRED DATA'
        # for element in paired_data:
        #     print element
        flight_dict = {}
        for k, v in paired_data:
            # print "ADDING", 'k',k, 'v', v
            dict_list = flight_dict.keys()
            # print dict_list
            # print k in dict_list
            if k in dict_list:
                make_list = [flight_dict[k]]
                # print "\nAlready there!", make_list
                make_list.append(v)
                # print "Added on:\n", make_list
                flight_dict[k] = make_list
                # print flight_dict.keys()
            else:
                flight_dict[k] = v
                # print flight_dict.keys()
        # Store new attributes to crash object
        if 'Site' in flight_dict.keys():
            crash_link.place = flight_dict['Site']
        if 'Crew' in flight_dict.keys():
            crash_link.crew = flight_dict['Crew']
        if 'Passengers' in flight_dict.keys():
            crash_link.passengers = flight_dict['Passengers']
        if 'Fatalities' in flight_dict.keys():
            crash_link.fatalities = flight_dict['Fatalities']
        if 'Total fatalities' in flight_dict.keys():
            crash_link.fatalities = flight_dict['Total fatalities']
        if 'Survivors' in flight_dict.keys():
            crash_link.survivors = flight_dict['Survivors']
        if 'Total survivors' in flight_dict.keys():
            crash_link.survivors = flight_dict['Total survivors']
        if 'Operator' in flight_dict.keys():
            crash_link.registration = flight_dict['Operator']
        if 'Registration' in flight_dict.keys():
            crash_link.registration = flight_dict['Registration']
        if 'Flight origin' in flight_dict.keys():
            crash_link.origin = flight_dict['Flight origin']
        if 'Destination' in flight_dict.keys():
            crash_link.destination = flight_dict['Destination']
        # return crash_html #, crash_html2
        # return {'name': name, 'country': country, 'time':time_in_gitmo}


if __name__ == '__main__':
    # QUESTION 1
    # Part A.
    crashes = make_dataframe()
    DATE='Date'
    CRASH='Crash'
    LINK='Link'
    BRIEF='Brief'
    scrape_link(crashes[CRASH])
    crashes[CRASH][0]
    # table_rows = crash_html.find('table', {'class' : 'infobox vcard vevent'}).find_all('tr')
    # data = []
    # for row in table_rows[2:]:
    #     print row
    #     new_tuple = row.get_text().strip().split('\n')
    #     key = new_tuple[0]
    #     value = new_tuple[1]
    #     if key =='Date':
    #         new_value = re.findall(r'(\d+)\-(\d+)\-(\d+)', value)
    #         new_date =  new_value[0][0] + new_value[0][1] + new_value[0][2]
    #         new_tuple[1] = new_date
    #     if key =='Site':
    #         new_tuple.pop()
    #     new_tuple[1] = re.sub(r'(\[\d+\])','', new_tuple[1])
    #     data.append(new_tuple)
    # flight_dict = {}
    # for k, v in data:
    #     flight_dict[k] = v
    # # Store new attributes to crash object
    # crash_link.place = flight_dict['Site']
    # crash_link.crew = flight_dict['Crew']
    # crash_link.passengers = flight_dict['Passengers']
    # crash_link.fatalities = flight_dict['Fatalities']
    # crash_link.passengers = flight_dict['Survivors']
    # crash_link.registration = flight_dict['Operator']
    # crash_link.origin = flight_dict['Flight origin']
    # crash_link.destination = flight_dict['Destination']
    # print data
    # for k, v in data:
    #     print v, k
    #
# ctext = 'https://en.wikipedia.org/wiki/1922_Picardie_mid-air_collision'
# source_code = requests.get(ctext)
# picard = BeautifulSoup(source_code.text, 'lxml')
# table_rows = picard.find('table', {'class' : 'infobox vcard vevent'}).find_all('tr')
# data = []
# for row in table_rows[2:]:
#     print row
#     new_tuple = row.get_text().strip().split('\n')
#     print new_tuple
#     data.append(new_tuple)
#     # new_tuple[1] = re.sub(r'(\[\d+\])','', new_tuple[1])
#
#     data.append(new_tuple)
# data
    # ctext = 'https://en.wikipedia.org/wiki/List_of_accidents_and_incidents_involving_commercial_aircraft/wiki/1919_Verona_Caproni_Ca.48_crash'
    # vtext = 'https://en.wikipedia.org/wiki/1919_Verona_Caproni_Ca.48_crash'
    # source_code = requests.get('https://en.wikipedia.org/wiki/1919_Verona_Caproni_Ca.48_crash')
    # verona = BeautifulSoup(source_code.text, 'lxml')
    # x = BeautifulSoup(link_html.text, 'lxml')
    # h1 = crash_html.find_all('h1')[0]
    # body = crash_html.find_all('div', {'class':'mw-body-content'})
    # t1 = crash_html.find_all('table')[0]
    # body = crash_html.find_all('div', {'class':'mw-body-content'})
    # data = []
    # table = crash_html.find('table') #, attrs={'class':'lineItemsTable'})
    # table = crash_html.find('table', {'class':'infobox-vcard-vevent'})
    # table_body = crash_html.find('table')
    # data2 = []
    # rows = crash_html.find_all('table')[1].find_all('tr')
    # for row in rows:
    #     cols = row.find_all('td')
    #     cols
    #     cols = [ele.text.strip() for ele in cols]
    #     data2.append([ele for ele in cols if ele]) # Get rid of empty values
    # crash_html = grab_link_like_person(base_url + index_ref + crash_links)
    # scrape_link(crashes[LINK][2])
    # url  = base_url + index_ref + crashes[LINK][2]
    # crash_html = urlopen(url)
    # crash_html = grab_link_like_person(base_url + index_ref + crashes[LINK][2])
# Define a function wrapper for grabbing

#

        # go to the link
        # save the stuff we care about
# prisoners = {}
# link_num = 0
# for link in prisoner_links:
#     link_num += 1
#     print link_num
#     # prisoners[link_num] = scrape_link[link]
# print prisoners
