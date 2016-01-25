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

crimes = pd.read_csv('2015_crimes.csv', parse_dates=['Date'])
ses = pd.read_csv('Census_Data_Selected_socioeconomic_indicators_in_Chicago_2008_2012.csv')

communityses = "Community Area Number"
cname = "COMMUNITY AREA NAME"
# (a) Calculate the number of crimes in each Community Area in 2015.
# Only presume that ses contains comprehensive community areas.
# Merge crimes by community area:
crimeses = crimes.merge(ses, left_on=community,
                        right_on=communityses,
                        how='outer') # I want that indicator oprion
                                     # in version 0.17.0. Grrr...

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
