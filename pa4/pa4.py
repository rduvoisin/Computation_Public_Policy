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

def grab_link_like_person(url, interval=5):
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

def scrape_link(crash_links):
    '''
    Input: a pandas dataframe of Crash objects.

    Calls grab_link_like_person on each Crash object's
    link attribute.

    Scrapes the first table of the link into a list of cleaned
    field-value texts for each row in table.

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
    count = -1
    for crash_link in crash_links:
        count += 1
        # Turn the link into an html file
        print count, ":\n",  crash_link.year, crash_link.date, base_url + crash_link.link
        link_html = grab_link_like_person(base_url + crash_link.link)
        crash_html = BeautifulSoup(link_html, 'lxml')
        table_rows = crash_html.find('table').find_all('tr')
        table = crash_html.find('table').get_text().strip().encode('utf-8')
        rows = table_rows
        row_tuples = [r.find_all(['th','td']) for r in rows]
        n_tuples = len(row_tuples)
        data = []
        # Compile tuples from table rows
        for row in row_tuples[2:]:
            for i in range(len(row)):
                row[i] = row[i].get_text().strip().encode('utf-8')
            if row[0] =='Site':
                row[1] = row[1].split('\n')[0]
            elif row[0] in ['Crew', 'Passengers', 'Survivors',
                                  'Fatalities', 'Total survivors',
                                  'Total fatalities']:
                print '\tSPECIAL', row[0], row
                row[1] = re.sub(r'(\[\d+\])','', row[1])
                # print  row[0], row
                pattern = re.compile('(\D*)(\d*)')
                number_string = row[1]
                anymatches = re.match(pattern, number_string)
                # print 'anymatches.groups()', anymatches.groups(), anymatches.groups()[1]
                if anymatches.groups()[1]:
                    row[1] = int(anymatches.groups()[1])
                else:
                    row[1] = None
            data.append(row)
        paired_data = [[element[0], element[1]] for element in data if len(element) > 1]
        flight_dict = {}
        # Compile data dictionary from table tuples
        for k, v in paired_data:
            dict_list = flight_dict.keys()
            if k in dict_list:
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
        print 'Place = ', crash_link.place, ',', crash_link.fatalities, ' killed.'

def attributes_to_columns(crash_data,
                          CRASH='Crash',
                          PLACE='Place', CREW='Crew',
                          PASSENGERS='Passengers',
                          FATALITIES='Fatalities',
                          SURVIVORS='Survivors',
                          REGISTRATION='Registration',
                          ORIGIN='Origin',
                          DESTINATION='Destination',
                          attributes={}
                          ):
    '''
    Inputs:
        - a dataframe that includes a column of
          Crash objects,
        - a dictionary of attributes to extract from
          the Crash objects column.

    Uses apply(lamda crash.attribute) to compile
    additional columns to the dataframe.

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
                      'destination': DESTINATION
                      }
    for k in attributes:
        crash_data[attributes[k]] = \
        crash_data[CRASH].apply(lambda c: c.get_attribute(k))
    print crash_data.columns, crash_data.index
    return crash_data


def strip_footnote(column_to_strip, within=True):
    '''Strips footnotes [d]'''
    column_to_strip.replace(regex=r'(\[\d+\])', value='', inplace=within)
    column_to_strip.replace(regex=r'(\(including 45 children\))', value='', inplace=within)

    # column_to_strip.apply(lambda x : re.sub(r'(\[\d+\])','', x))
    return column_to_strip


def strip_footnote_whole(dataframe):
    '''Strips footnotes from all columns \[d\]'''
    newdf = dataframe.copy()
    within = True
    for column in ['Crew', 'Passengers', 'Survivors', 'Fatalities']:
        print column
        newdf[column] = strip_footnote(newdf[column], within)
    return newdf


def sum_numbers_of_list(row, list=None):
    '''
    Helper for remove_alpha:

    Returns a numeric summation
    for a list of numbers.
    '''
    if list:
        numeric_list = list
    else:
        numeric_list = []
    if isinstance(row, (str, int, unicode)):
        if str(row):
            if str(row) == 'unknown':
                numeric_list.append(int('0'))
            elif str(row) == '60 (including 45 children)':
                numeric_list.append(int('60'))
            else:
                numeric_list.append(int(row))
        return sum(numeric_list)
    elif str(type(row)) == "<type 'list'>":
        if isinstance(row[0], (str, int, unicode)):
            for i in row:
                if str(i) == 'unknown':
                    numeric_list.append(int('0'))
                elif str(i) == '60 (including 45 children)':
                    numeric_list.append(int('60'))
                else:
                    numeric_list.append(int(i))
            total = sum(numeric_list)
            numeric_list  = []
            return total
        else:
            for i in row[1:]:
                numeric_list.append(int(i))
            return sum_numbers_of_list(row[0], numeric_list)
    return sum(numeric_list)


def remove_alpha(column_to_change, within=True):
    '''
    Removes words that aren't digits
    and sums lists of numbers.
    '''
    column_to_change.replace(regex=r'( \(including 45 children\)+)', value='', inplace=within)
    column_to_change.replace(regex=r'( \(all\)+)', value='', inplace=within)
    column_to_change.replace(regex=r'([a-zA-Z]+)', value='', inplace=within)
    column_to_change.replace(regex=r'(unknown)', value='0', inplace=within)
    column_to_change.replace(regex=r'(\(\d+)(.+)', value='\g<1>', inplace=within)
    column_to_change.replace(regex=r'(^\d+)(.+)', value='\g<1>', inplace=within)
    column_to_change.replace(regex=r'(\[\d+)( \(.+\))(.+\])', value='\g<1>\g<3>', inplace=within)
    column_to_change.replace(regex=r'([ \(+|\( |\(| \)|\) |\)])', value='', inplace=within)
    column_to_change.replace(regex=r'(\D)', value='', inplace=within)
    return column_to_change


def columns_to_totals(dataframe):
    '''Converts messy string data to numeric values'''
    newdf = dataframe.copy()
    within = True
    for column in ['Crew', 'Passengers', 'Survivors', 'Fatalities']:
        print column
        newdf[column] = remove_alpha(newdf[column], within)
        newdf[column] = newdf[column].apply(sum_numbers_of_list)
    return newdf


if __name__ == '__main__':
    # QUESTION 1
    # Part A.
    crashes = make_dataframe()
    DATE='Date'
    CRASH='Crash'
    LINK='Link'
    BRIEF='Brief'
    crashes = crashes.sort_values(by=[DATE])
    crashes.index = range(0, len(crashes))
    print 'Part A. By Origin:\n', crashes.head(10)
    # QUESTION 1
    # Part B.
    scrape_link(crashes[CRASH])
    crashed = crashes.copy()
    more_crashes = attributes_to_columns(crashed)
    print 'Part B. Append more columns:\n', more_crashes.columns, more_crashes.head(10)
    # QUESTION 1 Part C.
    # Which were the top 5 most deadly aviation incidents?
    # Report the number of fatalities and the flight origin for each.
    PLACE='Place'
    CREW='Crew'
    PASSENGERS='Passengers'
    FATALITIES='Fatalities'
    SURVIVORS='Survivors'
    REGISTRATION='Registration'
    ORIGIN='Origin'
    DESTINATION='Destination'
    unifat = more_crashes[FATALITIES].unique()
    FAT_INT = 'Fatalities_Int'
    numcrashes = more_crashes.copy()
    numcrashes = numcrashes.sort_values(by=[FATALITIES], ascending=False)
    numcrashes.index = range(0, len(crashes))
    print 'Part C. By Most Fatalities:\n' numcrashes[FATALITIES,ORIGIN][:10]
    # QUESTION 1 Part D
    # Which flight origin has the highest number of aviation
    # incidents in the last 25 years?
    by_origin = df.numcrashes.groupby([ORIGIN]).count()
    print 'Part D. By Origin:\n', by_origin
    # QUESTION 1 Part E.
    # Save this Dataframe as JSON and commit to your repo,
    # along with the notebook / python code used to do this assignment.
    import json
    json_dict = [{colname : row[i] for i, colname in enumerate(more_crashes.columns)} for row in more_crashes.iterrows()]
    json_dict
    json_crashes = json.dumps(json_dict)
    # run testing.py
    # more_crashes['Crew_Int'] = more_crashes['Crew']
    # more_crashed  = strip_footnote_whole(more_crashes)
    # more_crashes.head(20)
    # more_crashed.head(20)
    # more_crashed  = strip_footnote_whole(more_crashes)
    # some  = more_crashed[1:680]
    # num_crash = columns_to_totals(some)
    # num_crash.head(10)
    #
    # numcrash = num_crash.sort_values(by=[FATALITIES], ascending=False)
    # numcrash.head(10)
    # numcrash.describe()
    # passcrash= num_crash.sort_values(by=[PASSENGERS], ascending=False)
    # passcrash.head(50)
    # subfat = more_crashes[FATALITIES][0]
    # newfat = re.sub(r'(\[\d+\])','', subfat)
    # unique_fatalities = more_crashes[FATALITIES].unique()sort_values(by=[DATE])
