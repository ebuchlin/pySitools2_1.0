#! /usr/bin/python
"""

@author: Pablo ALINGERY for IAS 07-05-2013
"""

from sitools2.clients.sdo_client_idoc import *

d1 = datetime(2011,01,01,0,0,0)
d2 = d1 + timedelta(minutes=20)

sdo_data_list = search( DATES=[d1,d2], WAVES=['335','304'], CADENCE=['1 min'] ) 

#To limit the results sent by the server set nb_res_max
#sdo_data_list = search( DATES=[d1,d2], WAVES=['335','304'], nb_res_max= 5 ,CADENCE=['1 min'] ) 

#The fastest way to retrieve data
#PS : The directory 'results' has to be created !
get (MEDIA_DATA_LIST=sdo_data_list,TARGET_DIR='results', DECOMPRESS=True)

#Need to get a tar ball or zip file do sthg like :
#get_selection(MEDIA_DATA_LIST=sdo_data_list,DOWNLOAD_TYPE="tar", target_dir="results" ,FILENAME="my_download_file.tar")

#And if you want to specifies files name do sthg like 
#for item in sdo_data_list :
#	file_date_obs=item.date_obs
#	file_wave=item.wave
#	item.get_file( DECOMPRESS=False, FILENAME="toto_%s_%s.fits" %(file_date_obs,file_wave) , TARGET_DIR='results', QUIET=False )
