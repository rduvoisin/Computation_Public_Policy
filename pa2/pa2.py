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
import matplotlib.patches as patches

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
            self.__ses.dropna(subset = ['Community Area Number'], inplace=True)
            self.__crime = self.__crime[self.__crime[community]!=0]
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
day = 'Day'

# main
# Question 1: Crime counts and socioeconomics
#
# Download the crime data for all of the year 2015. Also download the socioeconomic data.

filenames = ['2015_crimes.csv',
            'Census_Data_Selected_socioeconomic_indicators_in_Chicago_2008_2012.csv']
crime_data = filenames[0]
ses_data = filenames[1]

chi = CityData(filenames, crime_data, ses_data)
chi.MakeCommunities(True)

# (a) Calculate the number of crimes in each Community Area in 2015.
# (b) Sort the Community Areas by 2015 crime count.
# Which Community Area (by name) has the highest crime count. The lowest?
cnames = chi.crimeses[cname].unique().tolist()
community_crime_count = chi.crimeses.groupby(cname)['ID'].agg('count').copy()
community_crime_count = pd.DataFrame({'Crime Count' :community_crime_count})
community_crime_count.sort_values('Crime Count', ascending=False, inplace=True)

print '1. a) Community Area Crime Counts:\n\tHighest: {} ({}),\n\tLowest: {} ({})'.\
format(community_crime_count.index[0], community_crime_count['Crime Count'][0],
            community_crime_count.index[76], community_crime_count['Crime Count'][76])



# Plot Question 1. b)
plt.close('all')
fig, ax = plt.subplots(figsize=(10,12))
doc = 'crime_count_bycommunity.png'
t = 'Crime Counts by Community Area, 2015'
ccount = 'Crime Count'
plt.title(t)

proxy_patches = []
proxy_labels = []
community_colors_list = []
for n in community_crime_count.index:
    community_colors_list.append(chi.get_community(n).color)
    if ((chi.get_community(n).count == community_crime_count[ccount].max())
        | (chi.get_community(n).count == community_crime_count[ccount][76])):
        proxy_patch = patches.Patch(color=chi.get_community(n).color)
        proxy_labels.append("{}, {}".format(chi.get_community(n).name,
                            chi.get_community(n).count))
        proxy_patches.append(proxy_patch)

xs = np.arange(community_crime_count.size)
w = 0.9
community_crime_count.plot(kind='barh', width=w, fontsize=8,
                           grid=True, color=community_colors_list, ax=ax)
plt.gca().invert_yaxis()
plt.legend(proxy_patches, proxy_labels)
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
# print table.to_string(na_rep ='')
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
community_crime_weeklycount.sort_values(ascending=False, inplace=True)

community_crime_weeklycountunstack = community_crime_weeklycount.unstack(cname)
community_crime_weeklycountunstack.fillna(0, inplace=True)

fig, ax = plt.subplots(figsize=(20,10))
t = 'Weekly Crime Counts by Community Area, 2015'
doc = 'weekly_crime_count_bycommunity.png'
month_dict = {1: 'January', 2:'February', 3:'March', 4:'April',
              5:'May', 6: 'June', 7: 'July', 8: 'August', 9:'September',
              10: 'October', 11:'November', 12:'December'}
community_colors_list = []
sort_interesting = []
plot_interesting = []
sort_interesting = [(chi.get_community(n).count, chi.get_community(n).name) for n in interesting_places]
sort_interesting.sort()
for (count, name) in sort_interesting:
    plot_interesting.append(name)
    community_colors_list.append(chi.get_community(name).color)


community_crime_weeklycountunstack[plot_interesting].plot(ax=ax, rot=90,
                                                            xticks=community_crime_weeklycountunstack.index,
                                                            color=community_colors_list,
                                                            title=t)

plt.gcf().tight_layout()
fig.savefig(doc)

# Area Plot
fig, ax = plt.subplots(figsize=(20,10))
t = 'Weekly Crime Counts by Community Area, 2015'
doc = 'weekly_crime_bycommunity_area.png'
community_crime_weeklycountunstack[plot_interesting].plot(ax=ax, kind='area',
                                                          color=community_colors_list,
                                                          title=t)
plt.gcf().tight_layout()
fig.savefig(doc)

# (d) By joining with the socioeconomic data,
# create a scatter plot of crime counts against per capita income.
# Summarize the relationship in words.
community_area_count= chi.crimeses.groupby(cname)['ID'].agg('count').copy()
community_area_crime = pd.DataFrame({'Crime Count': community_area_count})
community_area_crime.sort_values('Crime Count', ascending=False, inplace=True)
# Merge community_area_crime into demographics
demographics = chi.crimeses.copy()
dem_crime = demographics.merge(community_area_crime,
                              left_on=cname, right_index=True)


# Give dataframe a colors column for plotting community areas.
def set_color_column(com_name):
    '''Helper for creating a community-specific
    color in a dataframe.'''
    return chi.get_community(com_name).color

# Scatter crime count on area income
fig, ax= plt.subplots(figsize=(14,8))
t = 'Yearly Crime by Per Capita Income (77 Community Areas), 2015'
doc = 'crime_count_bypcincome.png'

dem_crime['Color']=dem_crime[cname].apply(set_color_column)
dem_crime.fillna(0, inplace=True)
dem_colors = dem_crime.Color.tolist()
dem_crime.plot(kind='scatter', x=pcincome, y='Crime Count', c=dem_colors, title=t, ax=ax)
ax.text(30000, 12000, 'Community crime associates negatively and weakly with per capita income,\
\ncontrolling for nothing else.')
plt.ylim(0)
plt.gcf().tight_layout()
fig.savefig(doc)


# Question 2: Community Area populations
#
# Download the census block population data and the Community Area tracts mapping.
#
# (a) Join these together using the fact that the last six digits of the tract
# id in the mapping data correspond to the first six digits of the block id.
# However, the data portal has a bug:
# if the block starts with a zero, that digit is missing!
def get_last6digits(anumber):
    return str(int(str(anumber)[-6:]))

def get_first6digits(anumber):
    return str(anumber)[:6]


cblock = 'CENSUS BLOCK'
tract = 'tract_id'
com_id = 'community_id'
prefix = 'prefix'
block_pop = 'TOTAL POPULATION'
community_pop = 'community_pop'

tracts = pd.read_csv('communitytracts.csv')
tracts = tracts.rename(columns={' community_id':com_id})
tracts[tract] = tracts[tracts.columns[0]]
del tracts[tracts.columns[0]]

tracts[prefix] = tracts[tract].apply(get_last6digits)
empty_tracts = tracts.loc[tracts.prefix.str.len()<6]
tracts = tracts.loc[tracts.prefix.str.len()>=6]

blocks = pd.read_csv('Population_by_2010_Census_Block.csv')
blocks[prefix] = blocks[cblock].apply(get_first6digits)

# Join geographic data.
geo = blocks.merge(tracts, on=prefix)
geo['community'] = geo[com_id].apply(chi.get_community)
geo[cname] = geo['community'].apply(lambda x: x.name)
geo['community'] = geo['community'].apply(lambda x: x.number)
ignore_communities = ['nan', 'CHICAGO']
missing_communities = filter(lambda x: str(x) not in ignore_communities,
                            [i for i in cnames if i not in geo[cname].unique().tolist()])
# sourced on Google
missing_populations = {'Edison Park' : 11187, 'Edgewater' : 56521, 'West Ridge' : 71942}

# (b) Calculate the total population in each Community Area.
geo_sum = geo.groupby(cname)[block_pop].aggregate('sum')
geo_sum= pd.DataFrame({'community_pop': geo_sum, cname: geo_sum.index})
for com in missing_communities:
    newf = pd.DataFrame({'community_pop' : pd.Series([missing_populations[com]], index=[com]), cname:com})
    geo_sum = geo_sum.append(newf, ignore_index=True)

geo_sum.sort_values(by=community_pop, ascending=False, inplace=True)
geo_sum.set_index(cname, inplace=True)

# Plot community populations
fig, ax= plt.subplots(figsize=(10,12))
t = 'Population by Community Area, 2010'
doc = 'population_bycommunity.png'

community_colors_list = []
proxy_patches = []
proxy_labels = []

for n in geo_sum.index:
    community_colors_list.append(chi.get_community(n).color)
    if n in interesting_places:
        proxy_patch = patches.Patch(color=chi.get_community(n).color)
        proxy_labels.append("{}, {}".format(chi.get_community(n).name,
                            int(geo_sum[geo_sum.index==n][community_pop].mean())))
        proxy_patches.append(proxy_patch)

w = 0.9

geo_sum.plot(kind='barh', width=w, fontsize=8, title=t, legend=False,
             grid=True, color=community_colors_list, ax=ax)
plt.legend(proxy_patches, proxy_labels)
plt.gca().invert_yaxis()
plt.gcf().tight_layout()
fig.savefig(doc)

# Question 3: Crime rates
#
# Using your answer to (2),
# calculate the crime rate (defined as crime count per thousand capita)
# for the city in 2015.
# Then reanswer (1a-d) with crime count replaced by crime rate.
# Summarize your findings in words.

# Merge all data thus far and create crime rate
rate = 'crime_rate'
ccount = 'Crime Count'
com_ob = 'Community Object'
dem_crime_map = dem_crime.merge(geo_sum, left_on=cname, right_index=True)
dem_crime_map[rate] = dem_crime_map[ccount] / (dem_crime_map[community_pop] / 1000)
dem_crime_map[com_ob] = dem_crime_map[cname].apply(chi.get_community)

# 1 a) & 1 b):
community_crime_rate = dem_crime_map.groupby(cname)[rate].agg('mean').copy()
community_crime_rate = pd.DataFrame({rate :community_crime_rate})
community_crime_rate.sort_values(rate, ascending=False, inplace=True)

plt.close('all')
fig, ax = plt.subplots(figsize=(10,12))
doc = 'crime_rate_bycommunity.png'
t = 'Yearly Crime Rate (per 1000 residents) by Community Area 2015'
plt.title(t)

proxy_patches = []
proxy_labels = []
community_colors_list = []
for n in community_crime_rate.index:
    community_colors_list.append(chi.get_community(n).color)
    if ((n == community_crime_rate.index[0])
        | (n == community_crime_rate.index[76])):
        proxy_patch = patches.Patch(color=chi.get_community(n).color)
        proxy_labels.append("{}, {:.2f}".format(chi.get_community(n).name,
                            community_crime_rate[community_crime_rate.index==n][rate].mean()))
        proxy_patches.append(proxy_patch)

w = 0.9
community_crime_rate.plot(kind='barh', width=w, fontsize=8,
                           grid=True, color=community_colors_list, ax=ax)
plt.gca().invert_yaxis()
plt.legend(proxy_patches, proxy_labels)
plt.gcf().tight_layout()
fig.savefig(doc)

# 1 c)
# Plot Daily Crime Rate on select communities
# First save population total into community objects (value)
for com in geo_sum.index:
    print com==chi.get_community(com).name
    if com == chi.get_community(com).name:
        chi.get_community(com).value = int(geo_sum[geo_sum.index==com][community_pop].mean())
# Generate a Daily Crime Count in dem_crime_map
daily_count = 'Daily_Count'
# Divide daily counts by population
daily_rate = 'Daily_Rate'
dailyrate = community_crime_dailyunstack.copy()
for com in dailyrate.columns:
    dailyrate[com] = dailyrate[com].apply(lambda x: x / (chi.get_community(com).value / 1000))

dailyrate.fillna(0, inplace=True)
# Reorder columns according to their median daily rate for plotting preference.
dailyrate.median().order(ascending=False)
dailyrate = dailyrate.reindex_axis(dailyrate.median().order(ascending=True).index,axis=1)

plt.close('all')
fig, ax = plt.subplots(figsize=(20,10))
t = 'Daily Crime Rate (crimes per 1000 residents) by Community Area, 2015'
doc = 'daily_crime_rate_bycommunity.png'
proxy_patches = []
proxy_labels = []
community_colors_list = []
plotting_communities = []
for com in dailyrate.columns:
    if com in interesting_places:
        plotting_communities.append(com)
        community_colors_list.append(chi.get_community(com).color)
        proxy_patch = patches.Patch(color=chi.get_community(com).color)
        proxy_labels.insert(0, "{}, {:.2f}".format(chi.get_community(com).name,
                            dailyrate[com].median()))
        proxy_patches.insert(0,proxy_patch)


dailyrate[plotting_communities].plot(ax=ax, kind='area', rot=90, color=community_colors_list, title=t)
plt.gcf().tight_layout()
plt.legend(proxy_patches, proxy_labels, title= 'Median Daily Rate')
fig.savefig(doc)

# Last duplicate of question 1 with crime rates instead of counts:
# Scatter crime rate on area income

plt.close('all')
fig, ax= plt.subplots(figsize=(14,8))
t = 'Yearly Crime Rate by Per Capita Income (77 Community Areas), 2015'
doc = 'crime_rate_bypcincome.png'

proxy_patches = []
proxy_labels = []
community_colors_list = []

for com in dem_crime_map[cname].unique().tolist():
    if com in interesting_places:
        community_colors_list.append(chi.get_community(com).color)
        proxy_patch = patches.Patch(color=chi.get_community(com).color)
        proxy_labels.append("{}, {:.2f}".format(chi.get_community(com).name,
                            dailyrate[com].median()))
        proxy_patches.append(proxy_patch)

dem_colors = dem_crime_map.Color.tolist()

dem_crime_map.plot(kind='scatter', x=pcincome, y=rate, c=dem_colors, title=t, ax=ax)
ax.text(20000, 1200, 'When controlling for population size,\n\
community crime still associates negatively, but more weakly,\n\
with per capita income, when controlling for nothing else.\n\
The slope is much flatter.')

plt.ylim(0)
plt.legend(proxy_patches, proxy_labels, title= 'Median Crime Rate of Communities of Interest')
plt.gcf().tight_layout()
fig.savefig(doc)

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
