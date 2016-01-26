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
import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# Question 1: Crime counts and socioeconomics
#
# Download the crime data for all of the year 2015. Also download the socioeconomic data.
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

crimes = pd.read_csv('2015_crimes.csv', parse_dates=['Date'])
ses = pd.read_csv('Census_Data_Selected_socioeconomic_indicators_in_Chicago_2008_2012.csv')
variables = crimeses.columns.tolist()

cnames = crimeses[cname].unique().tolist()
# Make a community area class to hold certain attributes stable in plottling.
class CommunityArea(object):
    '''Initiates a class to hold attributes of Chicago's
    77 Community Areas constant for formatting data visualizations;
    - name
    - number (1-77)
    - color
    - value - mutable anytime.
    - harship - hardship index
    - income - per capita income
    '''

    def __init__(self, name, number, color,
                 crime_count, arrests, hardship=None, income=None, plot_value=0):
        self.__name = name
        self.__number = number
        self.__color = color
        self.count = crime_count  # Public; mutable anytime.
        self.arrest = arrests  # Public; mutable anytime.
        self.types = types  # Public; mutable anytime.
        self.__hardship = hardship
        self.__income = income
        self.value = plot_value  # Public; mutable anytime.

    @property
    def name(self):
        return self.__name

    @property
    def number(self):
        return self.__number
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



# Define a function to initiate a series of CommunityArea objects.
def MakeCommunities(data):
    '''Given two columns of data, returns a
    list of CommunityArea instances.
    '''

    return None
np.unique(crimeses[[cname]].values).tolist()
namepd = np.unique(crimeses[[cname]].values).tolist()
# (a) Calculate the number of crimes in each Community Area in 2015.
# Only presume that ses contains comprehensive community areas.
# Merge crimes by community area:
crimeses = crimes.merge(ses, left_on=community,
                        right_on=communityses,
                        how='outer') # I want that indicator oprion
                                     # in version 0.17.0. Grrr...
crimes_by_community = crimeses.groupby(cname)
variables = crimeses.columns.tolist()
for comm in crimes_by_community.groups.keys(){


}
community_crime_count = crimes_by_community['ID'].agg('count')
community_crime_count.sort(ascending=False)
community_area_crime = pd.DataFrame({'Crime Count': community_crime_count})
print('1. a) Community Area Crime Counts:\n\tHighest: {} ({}),\n\tLowest: {} ({})'.
     format(community_crime_count.index[0],
            community_crime_count[0],
            community_crime_count.index[76],
            community_crime_count[76]))
plt.close('all')
fig = plt.figure(figsize=(10,12))
xlabels = community_crime_count.index[:].tolist()
doc = 'crime_count_bycommunity.png'
community_crime_count.plot(kind='bar',
                           title='Crime Counts by Community Area, 2015') #, labels=crimes[cname]



fig.savefig(doc)
plt.close('all')
def to_day(timestamp):
    return timestamp.replace(minute=0,hour=0, second=0)

def get_date(date):
    return date.to_datetime #(format='%Y%m%d', errors='coerce')

from operator import methodcaller
s = pd.Series(crimeses['Date'])
d = s[:258478].map(lambda x: x.strftime('%Y-%m-%d'))
# d[258478] = s[258478:258478].map(lambda x: x.strftime('%Y-%m-%d'))
crimeses['Day'] = d.to_frame()
plt.close('all')
community_crime_dailycount = crimeses.groupby([cname, 'Day'])
community_crime_dailycount = community_crime_dailycount['ID'].agg('count')
community_crime_dailyunstack = community_crime_dailycount.unstack(cname)
community_crime_dailyunstack.fillna(0, inplace=True)
# community_crime_dailyunstack.iloc(:,1).plot()
# plt.show()
# crimes_by_community = crimes.groupby('Community Area')
# print('crimes_by_community.groups\n',crimes_by_community.groups)
#
# (b) Sort the Community Areas by 2015 crime count. Which Community Area (by name) has the highest crime count. The lowest?
#
# (c) Create a table whose rows are days in the year and columns are the 77 Community Area crime counts. Select a few Communities that you are interested and plot time series.
#
# (d) By joining with the socioeconomic data, create a scatter plot of crime counts against per capita income. Summarize the relationship in words.
# Question 2: Community Area populations
#
# Download the census block population data and the Community Area tracts mapping.
#
# (a) Join these together using the fact that the last six digits of the tract id in the mapping data correspond to the first six digits of the block id. However, the data portal has a bug: if the block starts with a zero, that digit is missing!
#
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
