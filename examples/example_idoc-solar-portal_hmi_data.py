#! /usr/bin/env python
"""

@author: Pablo ALINGERY 
"""

from  sitools2.clients.sdo_client_medoc import *

d1 = datetime(2011,01,01,0,0,0)
d2 = d1 + timedelta(minutes=15)

sdo_data_list = media_search( DATES=[d1,d2], WAVES=['335','193'], CADENCE=['1 min'], nb_res_max=2 ) 

recnum_list = []
for item in sdo_data_list :
	recnum_list.append(str(item.recnum))

print recnum_list
meta=media_metadata_search(KEYWORDS=['date__obs','quality','cdelt1','cdelt2','crval1'], RECNUM_LIST=recnum_list)

print meta

