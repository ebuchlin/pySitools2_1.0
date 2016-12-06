#! /usr/bin/env python
"""

@author: Pablo ALINGERY 
"""

from  sitools2.clients.sdo_client_medoc import *

d1 = datetime(2016,01,01,0,0,0)
d2 = datetime(2016,06,01,0,0,0)

sdo_hmi_data_list = media_search( DATES=[d1,d2], SERIES='hmi.sharp_cea_720s_nrt', CADENCE=['1d'], nb_res_max=100 ) 

#build a recnum list
recnum_list=[item.recnum for item in sdo_hmi_data_list]

#Metadata info 
print recnum_list
meta=media_metadata_search(KEYWORDS=['date__obs','quality','cdelt1','cdelt2','crval1'],SERIES='hmi.sharp_cea_720s_nrt', RECNUM_LIST=recnum_list)
print meta

#Download data 
for data in sdo_hmi_data_list :
	data.get_file(target_dir='results', SEGMENT=['Br'])

