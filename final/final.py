
# coding: utf-8

# In[402]:

# Rebeccah Duvoisin
# Final Project CITES Traffic Data
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
import mechanize as mc
import cookielib

# Browser
br = mc.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mc._http.HTTPRefreshProcessor(), max_time=1)

# Want debugging messages?
br.set_debug_http(True)
br.set_debug_redirects(True)
br.set_debug_responses(True)

# from mechanize import Browser
base_url = "http://trade.cites.org"
index_ref = "/en/cites_trade/download?filters[time_range_start]=2015&filters[time_range_end]=2015&filters[exporters_ids][]=all_exp&filters[importers_ids][]=all_imp&filters[sources_ids][]=all_sou&filters[purposes_ids][]=all_pur&filters[terms_ids][]=all_ter&filters[selection_taxon]=taxon&filters[taxon_concepts_ids][]=&filters[reset]=&web_disabled="
index_html = urlopen(base_url + index_ref)

# Parsed version of html - that is what a BeautifulSoup object is.
index = BeautifulSoup(index_html, 'lxml')
index.head
cites_page = base_url + index_ref
print cites_page
type(br)
r = br.open(cites_page)
cites_read = r.read()
cites_read


# In[403]:

print '\nOPENED PAGE\n', cites_read
print br.title()


# In[404]:

# Find form to manipulate selections, get download report button object.
globe_form = br.global_form()
print '\nGLOBAL FORM\n', globe_form
print '\nSEE ALL CONTROLS:\n'
download_button = None
control_number = 0
for c in globe_form.controls:
    print '\n\t', control_number,'CONTROL:', 'Name =', c.name, ', Value:', c.value,           ', Type:', c.type, ', Read only?:', c.readonly, ', ID:', c.id
    try:
        print '\t\t',  c.attrs
    except:
        print ""
    if c.id == 'button_report':
        download_button = c
    control_number += 1


# In[405]:

# Find 'Select Output Type' and 'Select Report Type' Controls
output_control = None
report_control = None
writable_controls = [c for c in globe_form.controls if not c.readonly]
print '\nWRITEABLE CONTROLS'
control_number = 0
for c in writable_controls:
    print '\t', control_number,'CONTROL:', 'Name =', c.name, ', Value:', c.value, ', Type:', c.type, ', Read only?:', c.readonly
    control_number += 1
    if c.name == 'outputType':
        output_control = c
    elif c.name == 'report':
        report_control = c


# In[406]:

print '\nALL CONTROLS:', '\n\tDOWNLOAD BUTTON (Get Report):', download_button, '\n\t\tAttrs:', download_button.attrs,       '\n\n\tOUTPUT CONTROL:', output_control, '\n\t\tItems:', output_control.items,       '\n\n\tREPORT CONTROL:', report_control, '\n\t\tItems:', report_control.items


# In[407]:

# View radio outputType control items
csv_option = output_control.get('csv')
web_option = output_control.get('web')
comparative_option = report_control.get('comparative')
for option in [csv_option, web_option, comparative_option]:
    print '\nOPTION:', 'Name:', option.name, ', ID:', option.id, ', ATTRIBUTES', option.attrs, ', Selected?', option.selected
print '\nOUTPUT_CONTROL ITEMS', output_control.items
print '\nREPORT_CONTROL ITEMS', report_control.items


# In[408]:

#  Set output control item to csv instead of web
output_control.get('web').selected = False
output_control.get('csv').selected = True
for option in [csv_option, web_option, comparative_option]:
    print '\nOPTION:', 'Name:', option.name, ', ID:', option.id, ', ATTRIBUTES', option.attrs, ', Selected?', option.selected
print '\nOUTPUT_CONTROL ITEMS', output_control.items
print '\nREPORT_CONTROL ITEMS', report_control.items


# In[409]:

#  Create a second request object with the prefered output type
rq_with_csv = globe_form.click()
try:
    csv_response = mc.urlopen(rq_with_csv)
except mc.HTTPError, csv_response:
    pass
# csv_response = br.submit()
print '\nRESPONSE TO CSV REQUEST:\n', csv_response.geturl()
for name, value in csv_response.info().items():
    print '-{}:\t{}'.format(name.title(), value)

# new_link = csv_response.geturl()
# response = br.follow_link(new_link)
# print response.geturl()


# In[410]:

# Now click the 'Get Report' to download the csv file (get button's url)
print download_button.attrs
print download_button.disabled
print download_button.type
button_type = download_button.type
button_id = download_button.id
print 'BUTTON TYPE', button_type, ', BUTTON ID:', button_id
response = globe_form.click(type=button_type, nr=0)
print response


# In[411]:

# print '\nREAD RESPONSE TO CSV REQUEST:\n', csv_response.read()


# In[412]:

# globe_form = br.global_form()


# In[413]:

# Get img src of the button of corresponding id and type
all_inputs = index.find_all('button')
print '\nBUTTONS:', len(all_inputs), button_id
button_number = 0
download_button_src = None
for button in all_inputs:
    print '\nBUTTON', button_number,':',  button.attrs, button.id
    image = button.find('img')
    image_src = image.get('src')
    if 'id' in button.attrs:
        print button.attrs['id'] == button_id
        if button.attrs['id'] == button_id:
            download_button_src = image_src
            break
    print 'SRC', download_button_src
    try:
        print '\tIMAGE', image
        print '\tIMAGE SOURCE:', image_src
    except:
        pass
    button_number += 1
print '\nIMAGE SRC FILE CHOSEN:', download_button_src
# print base_url, index_ref,


# In[414]:

cwd = os.getcwd()
cwd


# In[448]:

# Now try clicking with found url
download_full_src = base_url + download_button_src
print download_full_src
# Retrieve file
all_links = {}
all_pds = all_links.copy()
gross_exports = "/cites_trade/exports/download?filters[time_range_start]=2015&amp;filters[time_range_end]=2015&amp;filters[exporters_ids][]=all_exp&amp;filters[importers_ids][]=all_imp&amp;filters[sources_ids][]=all_sou&amp;filters[purposes_ids][]=all_pur&amp;filters[terms_ids][]=all_ter&amp;filters[selection_taxon]=taxon&amp;filters[taxon_concepts_ids][]=&amp;filters[reset]=&amp;web_disabled=&amp;filters[report_type]=gross_exports&amp;filters[csv_separator]=comma"
gross_imports = "/cites_trade/exports/download?filters[time_range_start]=2015&amp;filters[time_range_end]=2015&amp;filters[exporters_ids][]=all_exp&amp;filters[importers_ids][]=all_imp&amp;filters[sources_ids][]=all_sou&amp;filters[purposes_ids][]=all_pur&amp;filters[terms_ids][]=all_ter&amp;filters[selection_taxon]=taxon&amp;filters[taxon_concepts_ids][]=&amp;filters[reset]=&amp;web_disabled=&amp;filters[report_type]=gross_imports&amp;filters[csv_separator]=comma"
confcomp = "/cites_trade/exports/download?filters[time_range_start]=2010&amp;filters[time_range_end]=2015&amp;filters[exporters_ids][]=all_exp&amp;filters[importers_ids][]=all_imp&amp;filters[sources_ids][]=109&amp;filters[purposes_ids][]=all_pur&amp;filters[terms_ids][]=all_ter&amp;filters[selection_taxon]=taxon&amp;filters[taxon_concepts_ids][]=&amp;filters[reset]=&amp;web_disabled=&amp;filters[report_type]=comptab&amp;filters[csv_separator]=comma"
conf_gexport = "/cites_trade/exports/download?filters[time_range_start]=2010&amp;filters[time_range_end]=2015&amp;filters[exporters_ids][]=all_exp&amp;filters[importers_ids][]=all_imp&amp;filters[sources_ids][]=109&amp;filters[purposes_ids][]=all_pur&amp;filters[terms_ids][]=all_ter&amp;filters[selection_taxon]=taxon&amp;filters[taxon_concepts_ids][]=&amp;filters[reset]=&amp;web_disabled=&amp;filters[report_type]=gross_exports&amp;filters[csv_separator]=comma"
conf_gimport = "/cites_trade/exports/download?filters[time_range_start]=2010&amp;filters[time_range_end]=2015&amp;filters[exporters_ids][]=all_exp&amp;filters[importers_ids][]=all_imp&amp;filters[sources_ids][]=109&amp;filters[purposes_ids][]=all_pur&amp;filters[terms_ids][]=all_ter&amp;filters[selection_taxon]=taxon&amp;filters[taxon_concepts_ids][]=&amp;filters[reset]=&amp;web_disabled=&amp;filters[report_type]=gross_imports&amp;filters[csv_separator]=comma"
all_links['gross_exports'] = gross_exports
all_links['gross_imports'] = gross_imports
all_links['confcomp'] = confcomp
all_links['conf_gexport'] = conf_gexport
all_links['conf_gimport'] = conf_gimport
for copied_link in all_links.keys():
    download_full_src = base_url + all_links[copied_link]
    f = br.retrieve(download_full_src)[0]
    fhandler = pd.read_csv(f)
    fhandler.to_csv(cwd+"/"+copied_link)
    fhandler.columns
    all_pds[copied_link] = fhandler
gexports = all_pds['gross_exports']
gimports = all_pds['gross_imports']
confcomp = all_pds['confcomp']
conf_gexport = all_pds['conf_gexport']
conf_gimport = all_pds['conf_gimport']
# fhandler
# with open('/home/studentuser/ppha_30530/final/exporeted_csv.csv', 'w') as f:
#     f.write(fhandler.read())


# In[523]:

# Top Gross Exporters
gexports.columns
top_gross_exporters = gexports.groupby('Country').size().sort_values(ascending=False)
top_gross = pd.DataFrame()
top_gross['Total Gross Exports 2015'] = top_gross_exporters
print top_gross.columns
print top_gross[:5]
top_gross.columns
top_gross['Country'] = top_gross.index.tolist()
top_gross.index = range(0, len(top_gross))
top_gross


# In[524]:

print gimports.columns
top_gross_importers = gimports.groupby('Country').size().sort_values(ascending=False)
# top_gross['Total Gross Imports 2015'] = top_gross_importers
totgi = 'Total Gross Imports 2015'
totge = 'Total Gross Exports 2015'
print top_gross.columns
top_gross_importers = pd.DataFrame(top_gross_importers)
# top_gross_importerss['Country'] = top_gross_importers.index
# top_gross_importerss[totgi] = top_gross_importers
# top_gross_importerss = top_gross_importers.to_frame()
print top_gross_importerss.columns
top_gross_importers['Country'] = top_gross_importers.index.tolist()
top_gross_importers[totgi] = top_gross_importers[top_gross_importers.columns[0]]
print top_gross_importers.columns
top_gross_importers.index = range(0, len(top_gross_importers))
print top_gross_importers.columns
top_gross_importers = top_gross_importers.drop([top_gross_importers.columns[0]], axis=1)
top_gross_importers
top_gross = top_gross.merge(top_gross_importers, on='Country', how='outer')

top_gross
# top_gross[totge] = top_gross[top_gross.columns[0]]
# print
# top_gross_importers
# top_gross
# top_gross_importers.index
# top_gross = top_gross.merge(top_gross_importers, on='Country', how='outer')
# top_gross_importers.index


# In[447]:

print confcomp.columns
byexporter = confcomp.groupby('Exporter')
byimporter = confcomp.groupby('Importer')
top_importers = byimporter.size().sort_values(ascending=False)
top_importer = pd.DataFrame()
top_importer['Total Imports (2010-)'] = top_importers
print top_importer.columns
print top_importer[:5]
top_exporter = pd.DataFrame()
top_exporters = byexporter.size().sort_values(ascending=False)
top_exporter['Total Exports (2010-)'] = top_exporters
print top_exporter.columns
print top_exporter[:5]


# In[425]:

conf_gexport


# In[419]:

conf_gimport


# In[420]:

# TRY MANUAL COPY
# Get img src of the button of corresponding id and type
# print response.geturl()
all_inputs = index.find_all('a', href=True)
# copied_link = "/cites_trade/exports/download?filters[time_range_start]=2015&amp;filters[time_range_end]=2015&amp;filters[exporters_ids][]=all_exp&amp;filters[importers_ids][]=all_imp&amp;filters[sources_ids][]=all_sou&amp;filters[purposes_ids][]=all_pur&amp;filters[terms_ids][]=all_ter&amp;filters[selection_taxon]=taxon&amp;filters[taxon_concepts_ids][]=&amp;filters[reset]=&amp;web_disabled=&amp;filters[report_type]=comptab&amp;filters[csv_separator]=comma"
print '\nA Tags:', len(all_inputs)
tag_number = 0
for i in all_inputs:
    print '\nTAG', tag_number,':',  i.attrs
    if 'id' in i.attrs:
        if i.attrs['id'] == 'download_genie':
            link = i.get('href')
            print 'MATCH',  i.attrs['id'], link
            print i
            break
#     links = i.find('a')
#     image_src = image.get('src')
#     if 'id' in button.attrs:
#         print button.attrs['id'] == button_id
#         if button.attrs['id'] == button_id:
#             download_button_src = image_src
#             break
#     print 'SRC', download_button_src
#     try:
#         print '\tIMAGE', image
#         print '\tIMAGE SOURCE:', image_src
#     except:
#         pass
#     button_number += 1
# print '\nIMAGE SRC FILE CHOSEN:', download_button_src
# print base_url, index_ref,


# In[525]:

conf_comp.head(50)


# In[ ]:
