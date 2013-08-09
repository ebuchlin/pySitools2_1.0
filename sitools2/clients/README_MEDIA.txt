#############################################  How to use python sdo_client_idoc.py  ######################################################
#version  1.0 #############################################################################################################################

This module has been designed to give python programmers an easy way to interrogate medoc-sdo.ias.u-psud.fr interface & to get data from it.

You can make a search with the following entries : a date range, a wavelength or multiple wavelengths, a cadence.
You will have as a result a list of Sdo_data objets. You can print each element to display its url, recnum, sunum, date_obs, wavelength,
ias_location, exptime and t_rec_index For each result you will be able to call the metadata_search() method in order to have additional 
metadata information. You can also call the function media_get() to download the data you are interested in.

Requirements: Python2.6 or greater & module pySitools2_idoc.py are needed.

################################################  HOWTO + Examples  #######################################################################

How to make a request to medoc-sdo.ias.u-psud.fr from python  ?

1 - In python, import everything from the module sdo_client_idoc :
from sdo_client_idoc import *

2-Choose your date range 
  Example : to search between 2012/11/21 and 2012/11/22 :

d1=datetime(2012,11,21,0,0,0)
d2=d1+timedelta(days=1)

3-Use the function media_search() 
  
  sdo_data_list = media_search(DATES=[d1, d2],WAVES=[waves_value], CADENCE=[cadence_value], NB_RES_MAX=limit_value ) where :

  * waves_value is the wavelength you are interested in, it can be in the list : '94','131','171','193','211','304','335','1600','1700'
    A list of value is also allowed, like for example WAVES=['304','131']
  * cadence_value can be : '1 min', '2 min', '5 min', '10 min', '30 min', '1 h', '2 h', '6 h', '12 h' , '1 day'
    or in the equilvalent list : '1m', '2m','5m','10m','30m','1h','2h','6h','12h', '1d'
    Only one cadence is allowed per request
  * limit_value is passed to force the server to give {limit_value} answers at most
  * Lower case as arguments are allowed too so 
    sdo_data_list=media_search(dates=[d1,d2],waves=[waves_value],cadence=[cadence_value], nb_res_max=limit_value) will do the same


Example: 
sdo_data_list=media_search(DATES=[d1,d2],WAVES=['335'],CADENCE=['2 min'], NB_RES_MAX=10) 

You will get a list of sdo_data objects. To see the content, you can simply call 'print item' 
Example:
for item in sdo_data_list:
	print item

You can also access a selected attribute from the list :
url, recnum, sunum, date_obs, wavelength, ias_location, exptime,t_rec_index

Example : To get the date_obs of the second item (index 1 in python) returned by the media_search : 
date_choosen = sdo_data_list[1].date_obs

LIMITATION : The media_search function gives 350000 outputs at most.


4-If you wish to have additional metadata information, use the metadata_search() method

  my_meta_search = item.metadata_search( KEYWORDS = metadata_list ) where :

  * item s a element of sdo_data_list
  * metadata_list is the list of keywords you are interested in 
  * Lower case as arguments are allowed too so
    my_meta_search = item.metadata_search( keywords = metadata_list ) will do the same

You will get for each request a python dictionary (i.e. a hash table).

To display the results, you can use :
print my_meta_search 

or print a selected parameter using for example:
print my_meta_search['quality']

 
For example, to have information on quality, cdelt1, cdelt2 and crval1, do :

for item in sdo_data_list:
	my_meta_search=item.metadata_search(keywords=['quality','cdelt1','cdelt2','crval1'])
	print my_meta_search



PS:
To discover all metadata available use the function metadata_info()
Example: 
print metadata_info()


5-To download data from medoc-sdo.ias.u-psud.fr
Since you have a result sdo_data_list from a previous media_search() request, you simply have to call the function media_get:

media_get (MEDIA_DATA_LIST=sdo_data_list,DECOMPRESS=decompress_value,TARGET_DIR=directory_name, QUIET=quiet_value)

  * sdo_data_list is a var in which the result of your previous media_search is stored (see previous 3-Use the function media_search() )
  * decompress_value is the Rice-compression option.
    It is set to 'False' by default, it needs to be set to 'True' to get Rice-uncompressed data.
    ############ USE WITH CAUTION : A SINGLE UNCOMPRESSED RECORD IS 32MB ##################
  * directory_name is the targeted directory. By design, files are retrieved in the current directory.
    It needs to be specified (to an existing directory) to get the fits files elsewhere.
  * quiet_value switches off logs returned by item.get_file(). By default, quiet_value is False.
    To retrieve data in a quiet mode set QUIET=True  
  * Lower case as arguments are allowed too so
    item.get_file( media_data_list=sdo_data_list, decompress=decompress_value, target_dir=directory_name, quiet=quiet_value ) will do the same

NB : 
I advise you to not specify FILENAME here, the default name would be activate
If you specify FILENAME here it will work, but do it carefully in a loop otherwise all the files returned would have the same names...

for example :

sdo_data_list = media_search( DATES=[d1,d2], WAVES=['335','304'], nb_res_max= 50 ,CADENCE=['1 min'] ) 
media_get (MEDIA_DATA_LIST=sdo_data_list,TARGET_DIR='results', DECOMPRESS=True)

5bis-To download data within a tar or a zip file from medoc-sdo.ias.u-psud.fr
Add the parameter DOWNLOAD_TYPE  as followed :
media_get(MEDIA_DATA_LIST=sdo_data_list,DOWNLOAD_TYPE=download_type_value,TARGET_DIR=directory_name,FILENAME=filename_value,QUIET=quiet_value)

  * download _type is the format of the file returned, it can value 'tar' or 'zip' (tar is faster than zip)
  * filename_value is None by default, the filename recorded will be 'IAS_SDO_export_{currentTimestamp}.{download_type_value}'.

6- Other way to download data from medoc-sdo.ias.u-psud.fr (FILENAME specification is better here)
Since you have a result sdo_data_list from a previous media_search() request, you simply have to call the method get_file:

for item in sdo_data_list:
	item.get_file( DECOMPRESS=decompress_value, FILENAME=filename_value, TARGET_DIR=directory_name, QUIET=quiet_value ) for each item (a Sdo_data object). 

  * decompress_value is the Rice-compression option.
    It is set to 'False' by default, it needs to be set to 'True' to get Rice-uncompressed data.
    ############ USE WITH CAUTION : A SINGLE UNCOMPRESSED RECORD IS 32MB ##################
  * filename_value is None by default, the filename recorded will be 'aia.lev1.{wave}A_{date_obs}.image_lev1.fits'.
    It needs to be specified if you want to change the downloaded file name.
  * target_dir is the targeted directory. By design, files are retrieved in the current directory.
    It needs to be specified (to an existing directory) to get the fits files elsewhere.
  * quiet_value switches off logs returned by item.get_file(). By default, quiet_value is False.
    To retrieve data in a quiet mode set QUIET=True  
  * Lower case as arguments are allowed too so
    item.get_file( decompress=decompress_value, filename=filename_value, target_dir=directory_name, quiet=quiet_value ) will do the same

For example :

sdo_data_list=media_search(DATES=[d1,d2],WAVES=['335'],CADENCE=['2 h']) 
for data in sdo_data_list :
		data.get_file(TARGET_DIR='results/')


################################ Complete example ###########################

# This example queries for all AIA files at 335 Angstrom between d1 and d2
# and only downloads files for which quality keyword is OK.

from sdo_client_idoc import *

d1 = datetime(2011,01,01,0,0,0)
d2 = d1 + timedelta(minutes=20)

sdo_data_list = media_search( DATES=[d1,d2], WAVES=['335','304'], CADENCE=['1 min'] ) 

#To limit the results sent by the server set nb_res_max
#sdo_data_list = media_search( DATES=[d1,d2], WAVES=['335','304'], nb_res_max= 5 ,CADENCE=['1 min'] ) 

#The simple way would be 
media_get (MEDIA_DATA_LIST=sdo_data_list,TARGET_DIR='results', DECOMPRESS=True)

#Need to get a tar ball or zip file do sthg like :
#media_get(MEDIA_DATA_LIST=sdo_data_list,DOWNLOAD_TYPE="tar", target_dir="results" ,FILENAME="my_download_file.tar")

#And if you want to specifies files name use get_file() method and do something like the following
#for item in sdo_data_list :
#	file_date_obs=item.date_obs
#	file_wave=item.wave
#	item.get_file( DECOMPRESS=False, FILENAME="toto_%s_%s.fits" %(file_date_obs,file_wave) , TARGET_DIR='results', QUIET=False )
