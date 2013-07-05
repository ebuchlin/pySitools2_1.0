#! /usr/bin/env python

#    SITools2 client for Python
#    Copyright (C) 2013 - Institut d'astrophysique spatiale
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
#get (MEDIA_DATA_LIST=sdo_data_list,TARGET_DIR='/tmp', DECOMPRESS=True)

#Need to get a tar ball or zip file do sthg like :
get_selection(MEDIA_DATA_LIST=sdo_data_list, TARGET_DIR="/tmp" ,FILENAME="my_download_file")

#And if you want to specifies files name do sthg like 
#for item in sdo_data_list :
#	file_date_obs=item.date_obs
#	file_wave=item.wave
#	item.get_file( DECOMPRESS=False, FILENAME="toto_%s_%s.fits" %(file_date_obs,file_wave) , TARGET_DIR='results', QUIET=False )
