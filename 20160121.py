import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
print("all loaded")
DIR = 'lecture-examples-master/'
crimes = pd.read_csv('pa1/dec_2015_crimes.csv', parse_dates=['Date'])
crimes
# Groupby: Given a key column, one can partition a table into groups:
crimes50_by_community = crimes.head(50).groupby('Community Area')
print('crimes50_by_community.groups\n',crimes50_by_community.groups)
crimes_by_community = crimes.groupby('Community Area')
print('crimes_by_community.groups\n',crimes_by_community.groups)
# Aggregate
# We can aggregate a column over the groups using an aggregate function.
#    * Built-in functions include 'sum' 'mean' 'median' 'mode' 'count' 'std' 'nunique'.
#    * Can also pass an arbitrary function whose argument is a vector and returns a scalar.
community_crime_count = crimes_by_community['ID'].agg('count')
community_crime_count
community_crime_count.plot(kind='bar', figsize=(12,5))
plt.show()

# Daily Timeseries
def to_day(timestamp):
    return timestamp.replace(minute=0,hour=0, second=0)

crimes['Day'] = crimes['Date'].apply(to_day)
crimes_by_day = crimes.groupby('Day')
crimes_by_day['ID'].agg('count').plot()
plt.show()

# What about a time series for a single community area?
crimes[crimes['Community Area'] == 41].groupby('Day')['ID'].agg('count').plot()
plt.show()
# Multiple Group By
# To get a series for each community area we could just loop over them.
# But there is a better way.
# Group by can take *multiple* keys, in this case community area and day.
# The result has a (row) *multi-index*.
crimes_by_community_day = crimes.groupby(['Community Area', 'Day'])
crimes_by_community_day_count = crimes_by_community_day['ID'].agg('count')
crimes_by_community_day_count
# Similarly for arrests, then we can take their quotient:
crimes_by_community_day_arrests = crimes_by_community_day['Arrest'].agg('sum')
community_day_arrest_prop = crimes_by_community_day_arrests / crimes_by_community_day_count
community_day_arrest_prop
# How can we plot multiple of these time series together? Unstacking
community_day_arrest_prop.unstack('Community Area')
# There are missing values after reshaping.
# That means there were no crimes in that area on that day so `fillna(0)`
community_arrest_timeseries = community_day_arrest_prop.unstack('Community Area')
community_arrest_timeseries.fillna(0, inplace=True)
community_arrest_timeseries
# Now we can plot multiple community area timeseries:
community_arrest_timeseries[[40,41,42]].plot()
plt.show()
# Another dataset
# Let's look at Chicago's affordable housing dataset
newfile = DIR + 'Affordable_Rental_Housing_Developments.csv'
housing = pd.read_csv(newfile)
housing
# Join
# What if we want to know the crime rate in the community for each housing development?
# We can find this using what's called a join or merge.
# First let's turn the community_crime_count Series into a DataFrame:
community_area_crime = pd.DataFrame({'Crime Count': community_crime_count})
community_area_crime

housing_crime = housing.merge(community_area_crime,
                              left_on='Community Area Number', right_index=True)
housing_crime

# Another aggregate
# We can pass other functions to aggregate:
community_housing = pd.DataFrame({
                                'Affordable Housing Units': housing.groupby(
                                'Community Area Number')['Units'].agg('sum')
                                })
community_housing
housing_crime_aggregate = community_housing.join(community_area_crime)
housing_crime_aggregate.shape
# Join types
# Why does the above join only have entries for 53 community areas? <br>
# Because `merge` defaults to a `left` join. There are four types of joins:
# - left (left is master), use only keys from left frame (SQL: left outer join)
# - right (right is master), use only keys from right frame (SQL: right outer join)
# - inner (DEFAULT), use intersection of keys from both frames (SQL: inner join)
# - outer , use union of keys from both frames (SQL: full outer join)

# In this case we want an `outer` join.
housing_crime_aggregate = community_housing.merge(
        community_area_crime, left_index=True, right_index=True, how='outer')
housing_crime_aggregate.shape
housing_crime_aggregate

# Rows without a corresponding row in the merge are filled with missing values.
# In our case those should be zeros, so we can `fillna(0)`.
housing_crime_aggregate.fillna(0, inplace=True)
housing_crime_aggregate.plot(kind='scatter', x='Affordable Housing Units', y='Crime Count')
plt.show()
