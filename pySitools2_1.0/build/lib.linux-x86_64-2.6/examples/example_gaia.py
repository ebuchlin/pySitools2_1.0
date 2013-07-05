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
from sitools2.clients.gaia_client_medoc import *

d1 = datetime(2012,8,10,0,0,0)
d2 = d1 + timedelta(days=1)

gaia_data_list = gaia_search( DATES=[d1,d2], NB_RES_MAX=10)  

for item in gaia_data_list :
	print item

#the fastest way to retrieve data
#PS : The directory TARGET_DIR has to be created
#gaia_get(GAIA_LIST=gaia_data_list, TARGET_DIR="/tmp")

#specify TYPE you want to  retrieve , it should be in list 'temp','em','width','chi2' (TYPE=['all'] will do as well ), FILENAME would be the default one 
#gaia_get(GAIA_LIST=gaia_data_list, TARGET_DIR="/tmp", TYPE=['temp','em'])

#Need to get a tar ball do sthg like :
gaia_get(GAIA_LIST=gaia_data_list, TARGET_DIR="/tmp" ,FILENAME="my_dowload_file", DOWNLOAD_TYPE="tar")

#Need to do it quietly (verbose is the default )
#gaia_get(GAIA_LIST=gaia_data_list, TARGET_DIR="/tmp",QUIET=True)


