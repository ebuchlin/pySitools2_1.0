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
from sitools2.clients.gaia_client_idoc import *

d1 = datetime(2012,8,10,0,0,0)
d2 = d1 + timedelta(days=1)

gaia_data_list = search( DATES=[d1,d2], nb_res_max=1 )  

#for item in gaia_data_list :
#	print item

#the fastest way to retrieve data
#PS : The directory 'results' has to be created !
get(GAIA_LIST=gaia_data_list, TARGET_DIR="/tmp")

#specify TYPE you want to  retrieve , it should be in list 'temp','em','width','chi2' (TYPE=['all'] will do as well ), FILENAME would be the default one 
#get(GAIA_LIST=gaia_data_list, TARGET_DIR="results", TYPE=['temp','em'])

#specify FILENAME you want to retrieve , it should be a dictionary with key within 'temp','em','width','chi2' and value can be whatever you want
#get(GAIA_LIST=gaia_data_list, TARGET_DIR="results", FILENAME={'temp' :'temp.fits','em':'em.fits'})

#Need to do it quietly 
#get(GAIA_LIST=gaia_data_list, TARGET_DIR="results",QUIET=True)

#########################Warning###########################
#specify both FILENAME and TYPE is not allowed 
#get(GAIA_LIST=gaia_data_list, TARGET_DIR="results", FILENAME={'temp' :'temp.fits','em':'em.fits'}, TYPE=['temp','em'])
###########################################################

#Need to get a tar ball do sthg like :
#get_selection(GAIA_LIST=gaia_data_list,DOWNLOAD_TYPE="tar", target_dir="results" ,FILENAME="my_dowload_file.tar")

