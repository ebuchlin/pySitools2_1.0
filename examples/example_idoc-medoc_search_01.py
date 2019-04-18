#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test idoc_medoc_search with keywords param
SDO aia.lev1 web interface to access solar data
"""

__author__ = "Pablo ALINGERY"

from datetime import datetime


from sitools2.clients.idoc_medoc_client import idoc_medoc_search, idoc_medoc_get

d1 = datetime(2016, 1, 1, 0, 0, 0)
d2 = datetime(2016, 1, 1, 5, 12, 0)
# d2 = d1 + timedelta(minutes=5)

# sdo_hmi_data_list=media_search(DATES=[d1,d2],series='hmi.sharp_cea_720s_nrt',
# cadence=['1h'],nb_res_max=10)
sdo_data_list = idoc_medoc_search(DATES=[d1, d2], WAVES=['335', '193'], CADENCE=['1m'], nb_res_max=2,
                                  keywords=['date__obs', 'quality', 'cdelt1', 'cdelt2', 'crval1', 'sunum', 'recnum'])

# Print results
for result in sdo_data_list:
    print(result)


# for data in sdo_data_list:
#   data.get_file(target_dir='results', segment=['image_lev1'])
# data.get_file(target_dir='results', IAS_PATH=True)
# Need to get a tar ball or zip file :
# A bit slower than the previous one
idoc_medoc_get(MEDIA_DATA_LIST=sdo_data_list, target_dir="results")

# And if you want to specifies files name do sthg like
# for item in sdo_data_list :
# print item.date_obs, item.wave , item.recnum, item.sunum, item.ias_location
# file_date_obs = item.date_obs.strftime('%Y-%m-%dT%H-%M-%S')
# #file_wave = item.wave
# item.get_file(DECOMPRESS=False, FILENAME="toto_%s_%s.fits" %(file_date_obs,
# file_wave) , TARGET_DIR='results', QUIET=False )

# Search meta data info
# for item in sdo_data_list:
# print item.date_obs
# my_meta_search = item.metadata_search(KEYWORDS=['date__obs','quality',
# 'cdelt1','cdelt2','crval1'])
# print my_meta_search
# if (my_meta_search['quality'] == 0) :
# item.display()
# item.get_file(TARGET_DIR='results')
