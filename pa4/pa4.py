# Rebeccah Duvoisin
# Assignment 4
from __future__ import  division
import os
import sys
import re as re
import time
from urllib import urlopen
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import datetime as dt
import json
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
        self._data = None


    @property
    def link(self):
        return self.__link

    @property
    def li(self):
        return self.__li

    @property
    def year(self):
        '''Accident Year.'''
        return self._year

    @property
    def date(self):
        '''Accident Date (Month and Day).'''
        return self._date

    @date.setter
    def date(self, newdate):
        self._date = newdate

    @property
    def brief(self):
        '''Brief description of the accident.'''
        return self._brief

    @property
    def place(self):
        '''Location of the accident.'''
        return self._place

    @place.setter
    def place(self, place_string):
        self._place = place_string

    @property
    def crew(self):
        '''
        Number of crew members aboard: maybe a string
        or a list of strings if involving multiple
        aircraft.
        '''
        return self._crew

    @crew.setter
    def crew(self, crew_string):
        self._crew = crew_string

    @property
    def passengers(self):
        '''
        Number of passengers aboard: maybe a string
        or a list of strings if involving multiple
        aircraft.
        '''
        return self._passengers

    @passengers.setter
    def passengers(self, passengers_string):
        self._passengers = passengers_string

    @property
    def fatalities(self):
        '''Number of fatalities.'''
        return self._fatalities

    @fatalities.setter
    def fatalities(self, fatalities_string):
        self._fatalities = fatalities_string

    @property
    def survivors(self):
        '''Number of survivors.'''
        return self._survivors

    @survivors.setter
    def survivors(self, survivors_string):
        self._survivors = survivors_string

    @property
    def registration(self):
        '''
        Flight egistration code: maybe a string
        or a list of strings if involving multiple
        aircraft.
        '''
        return self._registration

    @registration.setter
    def registration(self, registration_string):
        self._registration = registration_string

    @property
    def origin(self):
        '''
        Flight origin: maybe a string
        or a list of strings if involving multiple
        aircraft.
        '''
        return self._origin

    @origin.setter
    def origin(self, origin_string):
        self._origin = origin_string

    @property
    def destination(self):
        '''
        Flight destination: maybe a string
        or a list of strings if involving multiple
        aircraft.
        '''
        return self._destination

    @destination.setter
    def destination(self, destination_string):
        self._destination = destination_string

    @property
    def data(self):
        '''Raw data list of table tuples.'''
        return self._data

    @data.setter
    def data(self, data_list):
        self._data = data_list

    def get_attribute(self, string_name):
        if string_name == 'link':
            return self.__link
        elif string_name == 'li':
            return self.__li
        elif string_name == 'year':
            return self._year
        elif string_name == 'date':
            return self._date
        elif string_name == 'brief':
            return self._brief
        elif string_name == 'place':
            return self._place
        elif string_name == 'crew':
            return self._crew
        elif string_name == 'passengers':
            return self._passengers
        elif string_name == 'fatalities':
            return self._fatalities
        elif string_name == 'survivors':
            return self._survivors
        elif string_name == 'registration':
            return self._registration
        elif string_name == 'origin':
            return self._origin
        elif string_name == 'destination':
            return self._destination
        elif string_name == 'data':
            return self._data
        else:
            print 'Enter valid attribute name!'


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
                            header_brief = subbullet_li.contents[-1].encode('ascii', 'ignore')
                        else:
                            sub_text = sub_dater.group(2).strip().encode('ascii', 'ignore')
                            header_brief.append(re.search('(\w+)(.*)', sub_text).group(0).encode('ascii', 'ignore'))
                    else:
                        header_brief = subbullet_li.contents[-1].encode('ascii', 'ignore')
                        new_bullet_from_li(subbullet_li, header_lists_year_dics, year, sub_date, header_brief)
            else:
                strip_date = header_li.next_element[:-2].strip()
                header_dater = re.match('(^\w+ \w+)(.*)', strip_date)
                header_date = header_dater.group(1)
                header_text = header_li.get_text()
                header_brief = re.sub(strip_date, '', header_text, 1).strip().encode('ascii', 'ignore')
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


def fix_date_lists(row):
    '''
    Edits the date of the Crash objects
    according to the 'Date' column.
    '''
    row[CRASH].date = row[DATE]


def fix_base_link(row):
    '''Return a LINK column with full address'''
    newlink = base_url + row[LINK]
    row[LINK] = newlink
    return row[LINK]


def fix_unicode_lists(row, COLUMN, INDEX='Index_Copy'):
    '''Replaces all lists in COLUMN with a single value'''
    if isinstance(row[COLUMN], list):
        if row[COLUMN]:
            print '_N = {} ({}):'.format(row[INDEX], row[DATE]), COLUMN, \
                  '{} items:'.format(len(row[COLUMN])), row[COLUMN]
            if row[INDEX] % 2 == 0:
                selected_item = re.sub(r'(\[\d+\])', '', row[COLUMN][0])
            else:
                selected_item = re.sub(r'(\[\d+\])', '', row[COLUMN][-1])
            print "\t>>", selected_item
        else:
            selected_item = np.nan
        row[COLUMN] = selected_item
        return row[COLUMN]
    else:
        row[COLUMN] = row[COLUMN]
        return row[COLUMN]


def make_dataframe(pattern='h3',
                   DATE='Date', CRASH='Crash',
                   LINK='Link', BRIEF='Brief'):
    '''
    Make a pandas dataframe from a BeautifulSoup index,
    and a starting pattern.

    Inputs: A BeautifulSoup object to parse and initial pattern,
    such as a header type, as a starting node.

    Calls parse_crashes_to_dict to assemble a dictionary
    of parsed links of interest.

    Returns: A pandas dataframe of Crash objects, from which
        following columns are also derived from the Crash attributes:
        - DATE, from CRASH.date,
        - LINK, from CRASH.link,
        - BRIEF, from CRASH.brief
    '''
    print '\nQUESTION 1: Part A\n Parsing data into dictionary...'
    all_headers = index.find_all(pattern)
    crash_dict = parse_crashes_to_dict(all_headers)
    print '\nBuilding dataframe from dictionary...'
    crashes = dict_todataframe(crash_dict)
    crashes[DATE] = pd.to_datetime(crashes[DATE])
    crashes[LINK] = crashes[CRASH].apply(lambda c: c.link)
    crashes[BRIEF] = crashes[CRASH].apply(lambda c: c.brief)
    crashes.apply(fix_date_lists, axis=1)
    print '\nDataframe built:\n Shape:', \
            crashes.shape, '\n Columns:', \
            crashes.columns, '\n Head 10:\n', \
            crashes.head(10)
    return crashes


def grab_link_like_person(url, interval=4):
    '''
    Clicks a url address and sets of timer
    to ensure a specified rate limit for url requests
    to the target web server.

    Returns an opened url page to scrape  content.
    '''
    html = urlopen(url)
    # source_code = requests.get(url)
    time.sleep(interval)
    return html


def collapse_table(chosen_table):
    '''
    Helper for scrape_link:
    Input: an html table object
    Returns:
        - raw_data: a list of raw string tables cells for archive,
        - data: a list of processed string tables cells
            to be used in saving contents to Crash attributes.
    '''
    table_rows = chosen_table.find_all('tr')
    row_tuples = [r.find_all(['th','td']) for r in table_rows]
    data = []
    raw_data = []
    # Compile tuples from table rows
    for row in row_tuples[2:]:
        for i in range(len(row)):
            row[i] = row[i].get_text().strip().encode('ascii', 'ignore')
        if row[0] =='Site':
            raw_data.append(row)
            row[1] = row[1].split('\n')[0]
            data.append(row)
        elif row[0] in ['Destination', 'Flight origin',
                        'Operator', 'Registration']:
            row[1] = re.sub(r'(\[\d+\])','', row[1])
            raw_data.append(row)
            data.append(row)
        elif row[0] in ['Crew', 'Passengers', 'Survivors',
                              'Fatalities', 'Total survivors',
                              'Total fatalities']:
            raw_data.append(row)
            row[1] = re.sub(r'(\[\d+\])','', row[1])
            pattern = re.compile('(\D*)(\d*)')
            anymatches = re.match(pattern, row[1])
            if anymatches.groups()[1]:
                row[1] = int(anymatches.groups()[1])
            else:
                if (row[1] == 'all' or row[1] == '(all)'):
                    row[1] = np.nan
                else:
                    row[1] = 0
            data.append(row)
        else:
            pass
    return raw_data, data


def scrape_link(crash_links, verbose=True):
    '''
    Input: a pandas dataframe of Crash objects.

    Calls grab_link_like_person on each Crash object's
    link attribute.

    Scrapes the first table of class 'infobox' from
    the link into a list of cleaned field-value
    texts for each row in table.

    Builds a flight dictionary from the valid field-value list,
    into key:value pairs.

    Stores each valid key-value pair into the crash_object
    under the appropriate attribute:
        -Number of passengers
        -Number of crew
        -Number of fatalities
        -Number of survivors
        -Registration
        -Flight origin
        -Destination
    '''
    print '\nPart B. \nScrape data from links and save to Crash object attributes...\n'
    count = -1
    for crash_link in crash_links:
        count += 1
        # Turn the link into an html file
        link_html = grab_link_like_person(base_url + crash_link.link)
        crash_html = BeautifulSoup(link_html, 'lxml')
        all_tables = crash_html.find_all('table')
        chosen_table = None
        right_class = 'infobox'
        # Select the table of the correct class to scrape
        while not chosen_table:
            for tab in all_tables:
                key = 'class'
                if key in tab.attrs:
                    if right_class in tab[key]:
                        chosen_table = tab
                        break
        # Collect data from table
        raw_data, data = collapse_table(chosen_table)
        # Save raw data table to crash object
        crash_link.data = raw_data
        paired_data = [[element[0], element[1]] for element in data if len(element) > 1]
        # Compile data dictionary from data tuples
        flight_dict = {}
        for k, v in paired_data:
            dict_list = flight_dict.keys()
            if k in dict_list:
                if k in ['Crew', 'Passengers', 'Survivors',
                         'Fatalities', 'Total survivors',
                         'Total fatalities']:
                    summation = flight_dict[k]
                    if summation:
                        summation += v
                    else:
                        summation = v
                    flight_dict[k] = summation
                else:
                    make_list = [flight_dict[k]]
                    make_list.append(v)
                    flight_dict[k] = make_list
            else:
                flight_dict[k] = v
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
        if verbose:
            if verbose == 'light':
                if count % 10 == 0:
                    print count, ':', crash_link.date, crash_link.year
            else:
                print count, ':', crash_link.date,  crash_link.year, crash_link.link, 'Place =', crash_link.place, ',', crash_link.fatalities, 'killed.'
    print '...all data scraped.'


def attributes_to_columns(crash_data, CRASH='Crash', PLACE='Place', CREW='Crew',
                          PASSENGERS='Passengers', FATALITIES='Fatalities',
                          SURVIVORS='Survivors', REGISTRATION='Registration',
                          ORIGIN='Origin', DESTINATION='Destination', DATA ='Raw_Data',
                          attributes={}
                          ):
    '''
    Uses apply(lambda crash_object.get_attribute(name)) to populate
    additional columns to the dataframe.
    Inputs:
        - a dataframe that includes a column of
          Crash objects,
        - a dictionary of attributes to extract from
          the Crash objects column.
    Returns:
        - a dataframe with the additional
          row-wise attribute content.
    '''
    if not attributes:
        attributes = {'place': PLACE,
                      'crew': CREW,
                      'passengers': PASSENGERS,
                      'survivors': SURVIVORS,
                      'fatalities': FATALITIES,
                      'registration': REGISTRATION,
                      'origin': ORIGIN,
                      'destination': DESTINATION,
                      'data': DATA
                      }
    for k in attributes:
        crash_data[attributes[k]] = \
        crash_data[CRASH].apply(lambda c: c.get_attribute(k))
    print '\nPopulated attributes to additional columns:\n', \
        crash_data.columns
    print crash_data.describe()
    print '\nFinished Part B.\n'
    return crash_data


if __name__ == '__main__':
    # Declare constants
    DATE='Date'
    CRASH='Crash'
    LINK='Link'
    BRIEF='Brief'
    PLACE='Place'
    CREW='Crew'
    PASSENGERS='Passengers'
    FATALITIES='Fatalities'
    FATALITIESRAW='Fatalities_Raw'
    SURVIVORS='Survivors'
    REGISTRATION='Registration'
    ORIGIN='Origin'
    DESTINATION='Destination'
    DATA ='Raw_Data'
    INDEX = 'Index_Copy'
    # QUESTION 1
    # Part A.
    crashes = make_dataframe()
    crashes = crashes.sort_values(by=[DATE])
    crashes.index = range(0, len(crashes))
    crashes[INDEX] = crashes.index.tolist()
    # Part B.
    scrape_link(crashes[CRASH], verbose='light')
    # Copy partial dataframe for safety
    crashed = crashes.copy()
    crashes = attributes_to_columns(crashes)
    # Copy full dataframe for safety
    crashed = crashes.copy()
    # Apply formating fixes to new data
    crashes = crashes.fillna(value=np.nan)
    crashes[LINK] = crashes.apply(fix_base_link, axis=1)
    for COLUMN in ['Destination', 'Origin', 'Registration', 'Brief']:
        crashes[COLUMN] = crashes.apply(lambda row: fix_unicode_lists(row, COLUMN), axis=1)
    crashes.head(10)
    # Part C.
    # Which were the top 5 most deadly aviation incidents?
    # Report the number of fatalities and the flight origin for each.
    # Copy full dataframe for safety
    crashed = crashes.copy()
    crashed[INDEX] = crashed.index.tolist()
    crashes = crashes.sort_values(by=[FATALITIES], ascending=False)
    crashes.index = range(0, len(crashes))
    crashes[INDEX] = crashes.index.tolist()
    print '\nPart C. Sort By Most Fatalities:\n', \
        crashes[[FATALITIES,ORIGIN, DATE]][:5]
    print '\nFLIGHT ORIGIN WITH THE MOST FATALITIES:\n', crashes[ORIGIN][0], '({})'.format(crashes[FATALITIES][0]), \
      'REGISTERED AS:',crashes[REGISTRATION][0], '\n\nSUMMARY:\n'
    for i in range(len(crashes[[FATALITIES,ORIGIN, DATE]][:5])):
        print '\n{}.'.format(i + 1), crashes[DATE][i], \
                '\nDeparted from', crashes[ORIGIN][i], \
                'towards', crashes[DESTINATION][i], \
                '\nCrash occured in', crashes[PLACE][i], \
                '\nDescribed as:\n\t', crashes[BRIEF][i]
    # Save dataframe to csv for safety
    # mycsv = crashed.to_csv('crash_csv', encoding='ascii', 'ignore')
    mcsvnan = crashes.to_csv('crash_nan_csv', encoding='ascii')
    # Part D
    # Which flight origin has the highest number of aviation
    # incidents in the last 25 years?
    today = dt.date.today()
    yearsago25 = dt.date(today.year - 25, today.month, today.day)
    last_25years = crashes[crashes[DATE] >= yearsago25]
    by_origin = last_25years.groupby([ORIGIN]).size().sort_values(ascending=False)
    print '\nPart D. Total Incidents By Origin:\n', by_origin[:5]
    print '\nFLIGHT ORIGIN WITH THE MOST INCIDENTS:\n', by_origin[:1], '\n\nINCLUDES:\n'
    deadliest_origin = crashes[crashes[ORIGIN]=='Ninoy Aquino International Airport'][INDEX]
    deadliest_origin = deadliest_origin.tolist()
    deadliest_origin
    print len(deadliest_origin), 'incidents:'
    for i in range(len(deadliest_origin)):
        print '\n{}.'.format(i + 1), crashes[DATE][deadliest_origin[i]], \
                '\nDeparted from', crashes[ORIGIN][deadliest_origin[i]], \
                'towards', crashes[DESTINATION][deadliest_origin[i]], \
                '\nCrash occured in', crashes[PLACE][deadliest_origin[i]], \
                '\nDescribed as:\n\t', crashes[BRIEF][deadliest_origin[i]]
    # Part E.
    # Save this Dataframe as JSON and commit to your repo,
    # along with the notebook / python code used to do this assignment.
    # myjson = crashed_fix.to_json('crash_json', orient='index') DOESNT WORK.
        # In [185]: myjson = crashed_fix.to_json('crash_json', orient='index')
        # Segmentation fault
        # studentuser@data-science-rocks:~/ppha_30530/pa4$
    string_crashes = crashes.copy()
    string_crashes.describe()
    myjson = string_crashes.to_json('crash_renew_json') # Friday submission
