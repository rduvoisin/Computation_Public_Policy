#
# Computation for Public Policy: Assignment 2
#
#     Assigned: Friday, January 22, 2016
#     Due: By beginning of class Tuesday, February 2, 2016
#     Submit via GitHub
#
# Introduction
#
# In this assignment we will further explore the Chicago crime data.
# This time we will look at a larger portion of the data and augment
# our analysis by including data about socioeconomics, population, and police stations.
#
# To get credit for your answer, you must show in full the code that produced the answer.
from __future__ import division
import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import operator
import matplotlib.cm as cm


# Make a community area class to hold certain attributes stable in plottling.
class CommunityArea(object):
    '''
    Initiates a class to hold attributes of Chicago's
    77 Community Areas constant for formatting data visualizations;
    - name
    - number (1-77)
    - crime_count = total crimes in the data
    - arrests = total arrests in the data
    - crimes = unique list of primary types
    - primary = top crime type
    - harship - hardship index
    - income - per capita income
    - color
    - value - mutable anytime.
    '''

    def __init__(self, name, number, crime_count, arrests_count,
                 primary_list=None, primary_type=None, hardship=None,
                 income=None, color=None, plot_value=None):

        self.__name = name
        self.__number = number
        self.count = crime_count  # Public; mutable anytime.
        self.arrests = arrests_count  # Public; mutable anytime.
        self._crimes = primary_list  # Public; mutable anytime.
        self._primary = primary_type
        self.__hardship = hardship
        self.__income = income
        self.__color = color
        self._value = plot_value  # Public; mutable anytime.

    @property
    def name(self):
        return self.__name

    @property
    def number(self):
        return self.__number

    @property
    def crimes(self):
        return self._crimes

    @crimes.setter
    def crimes(self, list_of_crimes):
        if isinstance(list_of_crimes,(str, list)):
            if isinstance(list_of_crimes,str):
                list_of_crimes = [list_of_crimes]
            self._crimes = list_of_crimes

    @property
    def primary(self):
        return self._primary

    @primary.setter
    def primary(self, primary_string):
        self._primary = primary_string

    @property
    def color(self):
        '''An RGB color list.'''
        return self.__color

    @color.setter
    def color(self, color):
        if isinstance(color,(str, list, np.ndarray)):
            self.__color = color

    @property
    def hardship(self):
        return self.__hardship

    @hardship.setter
    def hardship(self, number):
        if isinstance(number, (int, float)):
            self.__hardship = number

    @property
    def income(self):
        return self.__income

    @income.setter
    def income(self, income):
        if isinstance(income, (int, float)):
            self.__income = income

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        if isinstance(val, (int, float)):
            self._value = val


def get_nice_colors(n_colors):
    '''Helper for MakeCommunities for fixed community colors.'''
    return cm.Accent([1 - (i/n_colors) for i in range(n_colors)])

def get_fx_from_param(dataframe, communityname, param_to_var, param):
    '''
    Helper for MakeCommunities parameter compiler:
        - Returns the appropriate Grouby attribute for
          each parameter.
    '''
    MEANS_INDEX = ['NUMBER', 'HARDSHIP','INCOME']
    COUNTS_INDEX = ['COUNT']
    SUMS_INDEX = ['ARRESTS']
    TOPS_INDEX = ['NAME', 'TOP']
    UNIQUE_INDEX = ['CRIMES']

    if param in MEANS_INDEX:
        return dataframe.get_group(communityname)[param_to_var[param]].mean()
    elif param in COUNTS_INDEX:
        return dataframe.get_group(communityname)[param_to_var[param]].count()
    elif param in SUMS_INDEX:
        return dataframe.get_group(communityname)[param_to_var[param]].sum()
    elif param in TOPS_INDEX:
        if communityname != 'CHICAGO':
            return dataframe.get_group(communityname)[param_to_var[param]].describe()['top']
    elif param in UNIQUE_INDEX:
        return dataframe.get_group(communityname)[param_to_var[param]].unique().tolist()


class CityData(object):
    '''
    Reads and processes csv files into a suite of dataset
    structures for staging plots and descriptive summaries.

    Inputs:
    - filename(s)
    - Optional crime and socioeconomic filename specifiers, optional working
      dataset object (pandas.DataFrame, pandas.Series, or numpy.array)

    Saves (if applicable):
    - datasets: a list of pandas.DataFrame objects.
    - crimes: crime data (pandas.DataFrame.)
    - ses: socioeconomic data (pandas.DataFrame.)
    - crimeses: an outer-merged pd.df of crime and ses data.
    - communities: a list of CommunityArea objects derived
                   from crimeses.
    '''
    def __init__(self, filenames, crime=None, ses=None, working=None):
        self.__filenames = self.__set_filenames(filenames)
        self.__datasets = self.__HoldAllDFs()
        self.__crime = self.__MakeCrimeDF(crime)
        self.__ses = self.__MakeSESDF(ses)
        self.__crimeses, self.variables = self.merge_crime_ses()
        self.working = working
        self.communities = []
        self.crimes_by_community = None
        self.community_crime_count = None


    def __set_filenames(self, filenames):
        if isinstance(filenames, (str)):
            return [filenames]
        elif isinstance(filenames, (list)):
            return filenames
        else:
            raise ValueError('filenames must be a string or a list.')
        print('filenames ', filenames, ' to ', self.__filenames)


    def __HoldAllDFs(self):
        datasets = []
        for filename in self.__filenames:
            newdataset = pd.read_csv(filename)
            datasets += [newdataset]
        return datasets


    def __MakeCrimeDF(self, crime):
        for filename in self.__filenames:
            if filename == crime:
                return pd.read_csv(crime, parse_dates=['Date'])


    def __MakeSESDF(self, ses):
        for filename in self.__filenames:
            if filename == ses:
                return pd.read_csv(ses)


    def merge_crime_ses(self):
        # Presume only ses data
        # contain comprehensive community areas.
        if not self.__crime.empty and not self.__ses.empty:
            merged =  self.__crime.merge(self.__ses, left_on=community,
                                    right_on=communityses,
                                    how='outer') # I want that indicator oprion
                                                 # in version 0.17.0. Grrr...
            varlist = merged[cname].unique().tolist()
            return merged, varlist


    def get_varlist(self):
        if not self.__crimeses.empty:
            return self.__crimeses[cname].unique().tolist()


    @property
    def crimes(self):
        return self.__crime

    @property
    def ses(self):
        return self.__ses

    @property
    def crimeses(self):
        return self.__crimeses

    @property
    def working(self):
        return self.working

    @working.setter
    def working(self, new_data):
        if isinstance(new_data, (np.ndarray, pd.DataFrame, pd.Series)):
            self.working = new_data


    def MakeCommunities(self, replace=None):
        '''
        Stores a series of CommunityArea objects within CityData.
        - Builds crime and ses by community area groupby object.
        - Initiates a CommunityArea object for each row, containing
          collapsed summary statistics.
        - Appends each CommunityArea object to CityData.communities list.
        '''

        if not self.__crimeses.empty:
            if replace:
                self.communities = []

            crimes_by_community = self.__crimeses.groupby(cname)
            self.crimes_by_community = crimes_by_community

            parameters = ['NAME', 'NUMBER', 'COUNT', 'ARRESTS',
                          'CRIMES', 'TOP', 'HARDSHIP', 'INCOME']

            param_to_var = {'NAME' : cname, 'NUMBER' : community,
                            'ARRESTS' : arrest, 'COUNT' : community,
                            'CRIMES' : primary, 'TOP' : primary,
                            'HARDSHIP' : hardship, 'INCOME' : pcincome}

            MEANS_INDEX = ['NUMBER', 'HARDSHIP','INCOME']
            COUNTS_INDEX = ['COUNT']
            SUMS_INDEX = ['ARRESTS']
            TOPS_INDEX = ['NAME', 'TOP']
            UNIQUE_INDEX = ['CRIMES']

            community_colors = get_nice_colors(crimes_by_community.ngroups)
            community_colors = community_colors.tolist()

            areas_list = crimes_by_community.groups.keys()
            areas_list.sort()
            for comm in areas_list:
                # crimes_by_community.groups[comm][0]
                param_to_value = {}
                print('community in dev...', comm)
                for comm_char in parameters:
                    param_to_value[comm_char] = get_fx_from_param(crimes_by_community, comm, param_to_var, comm_char)

                order_number = areas_list.index(comm)
                color = community_colors[order_number]

                # if order_number % 2 == 0:
                #     color = community_colors[order_number]
                # else:
                #     color = community_colors[-order_number]

                # print('dict', param_to_value.items())

                new_community = CommunityArea(comm, param_to_value['NUMBER'],
                                              param_to_value['COUNT'],
                                              param_to_value['ARRESTS'])

                new_community.crimes = param_to_value['CRIMES']
                new_community.primary = param_to_value['TOP']
                new_community.hardship = param_to_value['HARDSHIP']
                new_community.income = param_to_value['INCOME']
                new_community.color = color
                                            #   param_to_value['CRIMES'],
                                            #   param_to_value['TOP'],
                                            #   param_to_value['HARDSHIP'],
                                            #   param_to_value['INCOME'], color)

                print('ADDED', comm)
                self.communities.append(new_community)



    def get_community(self, name_or_number):
        '''Returns a CommunityArea object
           that corresponds to the supplied name
           or community area number.
           '''
        if isinstance(name_or_number, (str, int, float)):
            for comm in self.communities:
                if isinstance(name_or_number, str):
            		if comm.name == name_or_number:
            			return comm
                else:
                    if comm.number == name_or_number:
                    	return comm

# GLOBALS
n = "ID"
case = "Case Number"
date = "Date"
block = "Block"
iucr = "IUCR"
primary = "Primary Type"
description = "Description"
location = "Location Description"
arrest = "Arrest"
domestic = "Domestic"
beat = "Beat"
district = "District"
ward = "Ward"
community = "Community Area"
fbi = "FBI Code"
xcoord = "X Coordinate"
ycoord = "Y Coordinate"
year = "Year"
updated = "Updated On"
lat = "Latitude"
lon = "Longitude"
lat_lon = "Location"
pcincome = 'PER CAPITA INCOME '
hardship = 'HARDSHIP INDEX'
communityses = "Community Area Number"
cname = "COMMUNITY AREA NAME"

# main
# Question 1: Crime counts and socioeconomics
#
# Download the crime data for all of the year 2015. Also download the socioeconomic data.

filenames = ['2015_crimes.csv',
            'Census_Data_Selected_socioeconomic_indicators_in_Chicago_2008_2012.csv']
crime_data = filenames[0]
ses_data = filenames[1]

chi = CityData(filenames, crime_data, ses_data)
chi.MakeCommunities()

# (a) Calculate the number of crimes in each Community Area in 2015.
# (b) Sort the Community Areas by 2015 crime count.
# Which Community Area (by name) has the highest crime count. The lowest?
cnames = chi.crimeses[cname].unique().tolist()
community_crime_count = chi.crimeses.groupby(cname)['ID'].agg('count').copy
community_crime_count.sort(ascending=False)
print('1. a) Community Area Crime Counts:\n\tHighest: {} ({}),\n\tLowest: {} ({})'.
     format(community_crime_count.index[0],
            community_crime_count[0],
            community_crime_count.index[76],
            community_crime_count[76]))



# Plot Question 1. b)
plt.close('all')
fig = plt.figure(figsize=(10,12))
doc = 'crime_count_bycommunity.png'
t = 'Crime Counts by Community Area, 2015'
plt.title(t)

community_colors_list = []
for n in community_crime_count.index:
    community_colors_list.append(chi.get_community(n).color)

xs = np.arange(community_crime_count.size)
w = 0.9
community_crime_count.plot(kind='barh', width=w, fontsize=8,
                           grid=True, color=community_colors_list)
plt.gca().invert_yaxis()

plt.gcf().tight_layout()
fig.savefig(doc)

# (c) Create a table whose rows are days in the year and columns are the
# 77 Community Area crime counts. Select a few Communities
# that you are interested and plot time series.
s = pd.Series(chi.crimeses['Date'])
d = s[:258478].map(lambda x: x.strftime('%Y-%m-%d'))

chi.crimeses['Day'] = d.to_frame()
# Table = Pivot
interesting_places = ['Hyde Park', 'South Chicago',
                      'South Lawndale', 'Lower West Side',
                      'Washington Park', 'Lake View', 'Roseland',
                      'Armour Square', 'Austin', 'Edison Park']

daily_table = chi.crimeses[['ID', cname, 'Day']].copy()
table = pd.pivot_table(daily_table, columns=cname, index=['Day'], aggfunc='count')
print table.to_string(na_rep ='')
daily_table = daily_table[daily_table[cname].isin(interesting_places)]
table = pd.pivot_table(daily_table, columns=cname, index=['Day'], aggfunc='count')
print table.to_string(na_rep ='')

# Plot Daily Counts on select communities
community_crime_dailycount = chi.crimeses.groupby([cname, 'Day'])
community_crime_dailycount = community_crime_dailycount['ID'].agg('count')
community_crime_dailyunstack = community_crime_dailycount.unstack(cname)
community_crime_dailyunstack.fillna(0, inplace=True)

community_colors_list = []
for n in interesting_places:
    community_colors_list.append(chi.get_community(n).color)


fig, ax = plt.subplots(figsize=(20,10))
t = 'Daily Crime Counts by Community Area, 2015'
doc = 'daily_crime_count_bycommunity.png'

community_crime_dailyunstack[interesting_places].plot(ax=ax, rot=90,
                                                      color=community_colors_list, title=t)
plt.gcf().tight_layout()
fig.savefig(doc)

# Too busy, smooth into week data
month_dict = {1: 'January', 2:'February', 3:'March', 4:'April',
              5:'May', 6: 'June', 7: 'July', 8: 'August', 9:'September',
              10: 'October', 11:'November', 12:'December'}

def get_value_label(value, value_dict=month_dict):
    if str(value) == 'nan':
        return None
    return value_dict[int(value)]

chi.crimeses['Week'] = chi.crimeses['Date'].dt.week
chi.crimeses['Month'] = chi.crimeses['Date'].dt.month
chi.crimeses['Month'] = chi.crimeses['Month'].apply(get_value_label)

community_crime_dates = chi.crimeses[['ID', cname, community, 'Week', 'Month']]

def print_full(x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')

community_crime_weeklycount = community_crime_dates.groupby([cname, 'Week'])
community_crime_weeklycount = community_crime_weeklycount['ID'].agg('count')
community_crime_weeklycountunstack = community_crime_weeklycount.unstack(cname)
community_crime_weeklycountunstack.fillna(0, inplace=True)

fig, ax = plt.subplots(figsize=(20,10))
t = 'Weekly Crime Counts by Community Area, 2015'
doc = 'weekly_crime_count_bycommunity.png'
month_dict = {1: 'January', 2:'February', 3:'March', 4:'April',
              5:'May', 6: 'June', 7: 'July', 8: 'August', 9:'September',
              10: 'October', 11:'November', 12:'December'}
community_crime_weeklycountunstack[interesting_places].plot(ax=ax, rot=90,
                                                            xticks=community_crime_weeklycountunstack.index,
                                                            color=community_colors_list,
                                                            title=t)

plt.gcf().tight_layout()
fig.savefig(doc)



#
# (d) By joining with the socioeconomic data, create a scatter plot of crime counts against per capita income. Summarize the relationship in words.
# Question 2: Community Area populations
#
# Download the census block population data and the Community Area tracts mapping.
#
# (a) Join these together using the fact that the last six digits of the tract id in the mapping data correspond to the first six digits of the block id. However, the data portal has a bug: if the block starts with a zero, that digit is missing!

# (b) Calculate the total population in each Community Area.
# Question 3: Crime rates
#
# Using your answer to (2), calculate the crime rate (defined as crime count per thousand capita) for the city in 2015. Then reanswer (1a-d) with crime count replaced by crime rate. Summarize your findings in words.
# Question 4: Crime and Police Stations
#
# Download the police stations data.
#
# (a) Extract the latitudes and longitudes of the police stations (found in the ADDRESS column) as floats into their own columns called 'Station Latitude' and 'Station Longitude', respectively.
#
# (b) Join the crime data with the stations on police district. Hint: the station district is a text field (because one of them is 'Headquarters') so you'll need to convert the crime district to the same.
#
# (c) Define a function which calculates the distance in kilometers between two points (latitude, longitude) using the Pythagorean theorem.
#
# Hint: To convert the coordinate distance to kilometers multiply by 95. For example the distance from (41, -87) to (41.1,-87) is about 9.5km. This is the scale factor for these coordinates near Chicago. Note this method is approximate because the scale factor varies from point to point (i.e. the Earth is not flat!).
#
# (d) Calculate the distance between each crime and its district police station. Hint: If your answer to (c) is of the form
#
# def distance(row):
# crime_lat = row['Latitude']
# crime_lon = row['Longitude']
# station_lat = row['Station Latitude']
# station_lon = row['Station Longitude']
# ...
# Then you can simply do
# df.apply(distance, axis=1)
#
# (e) Plot a histogram of crime count against distance to district police station. Summarize the relationship in words.
