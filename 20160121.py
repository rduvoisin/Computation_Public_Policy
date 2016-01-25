import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
print("all loaded")
crime = pd.read_csv('pa1/dec_2015_crimes.csv', parse_dates=['Date'])
crime
# Groupby: Given a key column, one can partition a table into groups:
crimes50_by_community = crimes.head(50).groupby('Community Area')
print('crimes50_by_community.groups\n',crimes50_by_community.groups)
crimes_by_community = crimes.groupby('Community Area')
print('crimes_by_community.groups\n',crimes_by_community.groups)
# Aggregate
#
# We can aggregate a column over the groups using an aggregate function.
#    * Built-in functions include 'sum' 'mean' 'median' 'mode' 'count' 'std' 'nunique'.
#    * Can also pass an arbitrary function whose argument is a vector and returns a scalar.
