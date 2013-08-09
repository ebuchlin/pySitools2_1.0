#############################################  How to use python gaia_client_idoc.py  ######################################################
#version  1.0 #############################################################################################################################

This module has been designed to give python programmers an easy way to interrogate medoc-dem.ias.u-psud.fr interface & to get data from it.

You can make a search with a date range as an entry parameter.
You will have as a result a list of gaia_data objets. You can print each element to display its attributes :
download, sunum_193, date_obs, filename, temp_fits_rice_uri, em_fits_rice_uri, width_fits_rice_uri and chi2_fits_rice_uri.
You can also call the function gaia_get() to download the data you are interested in.

Requirements: Python2.6 or greater & module pySitools2_idoc.py are needed.

################################################  HOWTO + Examples  #######################################################################

How to make a request to medoc-dem.ias.u-psud.fr from python  ?

1 - In python, import everything from the module gaia_client_idoc :
from gaia_client_idoc import *

2-Choose your date range 
  Example : to search between 2012/11/21 and 2012/11/22 :

d1=datetime(2012,11,21,0,0,0)
d2=d1+timedelta(days=1)

3-Use the function gaia_search() 
  
  gaia_data_list = gaia_search(DATES=[d1, d2] NB_RES_MAX=limit_value ) where :

  * limit_value is passed to force the server to give {limit_value} answers at most
  * Lower case as arguments are allowed too so 
    gaia_data_list=gaia_search(dates=[d1,d2], nb_res_max=limit_value) will do the same


Example: 
gaia_data_list=gaia_search(DATES=[d1,d2], NB_RES_MAX=10) 

You will get a list of gaia_data objects. To see the content, you can simply call 'print item' 
Example:
for item in gaia_data_list:
	print item

You can also access a selected attribute from the list :
download, sunum_193, date_obs, filename, temp_fits_rice_uri, em_fits_rice_uri, width_fits_rice_uri and chi2_fits_rice_uri

Example : To get the date_obs of the second item (index 1 in python) returned by the gaia_search : 
date_choosen = gaia_data_list[1].date_obs

LIMITATION : The gaia_search function gives 350000 outputs at most.

4-To download data from medoc-dem.ias.u-psud.fr
Since you have a result stored in the variable gaia_data_list from a previous gaia_search() request, you simply have to call the function gaia_get:

gaia_get (GAIA_LIST=gaia_data_list,TARGET_DIR=directory_name, QUIET=quiet_value)

  * gaia_data_list is a var in which the result of your previous gaia_search is stored (see previous 3-Use the function gaia_search() )
  * directory_name is the targeted directory. If not specifed files will be retrieved in the current directory.
    It needs to be specified (to an existing directory) to get the fits files elsewhere.
  * quiet_value switches off logs the verbose mode. By default, quiet_value is False.
    To retrieve data in a quiet mode set QUIET=True  
  * Lower case as arguments are allowed too so
    gaia_get( gaia_list=gaia_data_list, target_dir=directory_name, quiet=quiet_value ) will do the same


for example :

gaia_data_list = gaia_search( DATES=[d1,d2] ) 
gaia_get (GAIA_LIST=sdo_data_list,TARGET_DIR='results')

4bis-To download data within a tar file from medoc-dem.ias.u-psud.fr
Add the parameter DOWNLOAD_TYPE as followed :
	 
gaia_get(GAIA_LIST=gaia_data_list,DOWNLOAD_TYPE=download_type_value,TARGET_DIR=directory_name,FILENAME=filename_value,QUIET=quiet_value)

   * download _type is the format of the file returned, it can only value 'tar' for the moment no zip file file available so far.
   * filename_value is None by default, the filename recorded will be 'IAS_SDO_export_{currentTimestamp}.{download_type_value}'.

For example : 

gaia_data_list = gaia_search( DATES=[d1,d2] )
gaia_get(GAIA_LIST=gaia_data_list,DOWNLOAD_TYPE="tar", target_dir="results" ,FILENAME="my_dowload_file.tar")


5- You can choose also to download a certain TYPE of data from medoc-dem.ias.u-psud.fr
You just have to specify the TYPE you want to  retrieve , it should be a list among : 'temp','em','width','chi2' (TYPE=['all'] will do as well), the filess retrieved will have the default name 

gaia_get(GAIA_LIST=gaia_data_list, TARGET_DIR=directory_name, TYPE=type_list, QUIET=quiet_value)

  * gaia_data_list is a var in which the result of your previous gaia_search is stored (see previous 3-Use the function gaia_search() ).
  * directory_name is the targeted directory. If not specifed files will be retrieved in the current directory.
    It needs to be specified (to an existing directory) to get the fits files elsewhere.
  * type_list is output wanted, it has to be a list among : 'temp','em','width','chi2'.
  * quiet_value switches off logs the verbose mode. By default, quiet_value is False.
    To retrieve data in a quiet mode set QUIET=True  
  * Lower case as arguments are allowed too so
    gaia_get( gaia_list=gaia_data_list, target_dir=directory_name, type=type_list, quiet=quiet_value ) will do the same
  
for example :

gaia_data_list = gaia_search( DATES=[d1,d2] )
gaia_get(GAIA_LIST=gaia_data_list, TARGET_DIR="results", TYPE=['temp','em'])


6-May you require to need specific file names as outputs, you just have to specify FILENAME as a parameter 
FILENAME should be a dictionary. So the gaia_get function would seem like :

gaia_get(GAIA_LIST=gaia_data_list, TARGET_DIR=directory_name, FILENAME={type_value1 :'name_file1','type_value2':'name_file2'})

  * gaia_data_list is a var in which the result of your previous gaia_search is stored (see previous 3-Use the function gaia_search() ).
  * directory_name is the targeted directory. If not specifed files will be retrieved in the current directory.
    It needs to be specified (to an existing directory) to get the fits files elsewhere.
  * type_value1 or type_value#n is a key among : 'temp','em','width','chi2'.
  * name_file1 or name_file#n can value whatever you want for example : temp.fits 
  * Lower case as arguments are allowed too so
    gaia_get( gaia_list=gaia_data_list, target_dir=directory_name, type=type_list, quiet=quiet_value ) will do the same
  
for example :

gaia_data_list = gaia_search( DATES=[d1,d2] )
gaia_get(GAIA_LIST=gaia_data_list, TARGET_DIR="results", FILENAME={'temp' :'temp.fits','em':'em.fits'})

#########################Warning###########################
#specify both FILENAME and TYPE is not allowed 
#It would raise an error
###########################################################


################################ Complete example ###########################

# This example queries GAIA-DEM between d1 and d2
# and only downloads files for which quality keyword is OK.

from gaia_client_idoc import *

d1 = datetime(2012,8,10,0,0,0)
d2 = d1 + timedelta(days=1)

gaia_data_list = gaia_search( DATES=[d1,d2], nb_res_max=1 )  

#for item in gaia_data_list :
#	print item

#the fastest way to retrieve data
#PS : The directory 'results' has to be created !
gaia_get(GAIA_LIST=gaia_data_list, TARGET_DIR="results")

#specify TYPE you want to  retrieve , it should be in list 'temp','em','width','chi2' (TYPE=['all'] will do as well ), FILENAME would be the default one 
#gaia_get(GAIA_LIST=gaia_data_list, TARGET_DIR="results", TYPE=['temp','em'])

#specify FILENAME you want to retrieve , it should be a dictionary with key within 'temp','em','width','chi2' and value can be whatever you want
#gaia_get(GAIA_LIST=gaia_data_list, TARGET_DIR="results", FILENAME={'temp' :'temp.fits','em':'em.fits'})

#Need to do it quietly 
#gaia_get(GAIA_LIST=gaia_data_list, TARGET_DIR="results",QUIET=True)

#Need to get a tar ball do sthg like :
#gaia_get(GAIA_LIST=gaia_data_list,DOWNLOAD_TYPE="tar", target_dir="results" ,FILENAME="my_dowload_file.tar")

#To specify FILENAME you want to retrieve, use get_file() method and do something like the following
#FILENAME should be a dictionary with key within 'temp','em','width','chi2' and value can be whatever you want
#for item in gaia_data_list :
#	file_date_obs=(item.date_obs).strftime("%Y-%m-%dT%H:%M:%S")
#	item.get_file(TARGET_DIR="results", FILENAME={'temp' :"temp_%s.fits" % file_date_obs, 'em':"em_%s.fits" % file_date_obs})
#########################Warning###########################
#specify both FILENAME and TYPE is not allowed 
#gaia_get(GAIA_LIST=gaia_data_list, TARGET_DIR="results", FILENAME={'temp' :'temp.fits','em':'em.fits'}, TYPE=['temp','em'])
###########################################################


