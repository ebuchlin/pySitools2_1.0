#! /usr/bin/env python
"""
This script has been designed to give python programmers an easy way to interrogate media sitools2 interface.
You can make a search with the following entries : a date range , a wavelenghth or multiple wavelengths , a cadence.
You will have as a result a list of Sdo_data objets on which you can apply the method display() that will give you for each 
the recnum, the sunum, the date_obs, the wavelength, the ias_location, the exptime and t_rec_index 
For each result you will be able to call metadata_search() method in order to have the metadata information.
@author: Pablo ALINGERY for IAS 28-08-2012
"""
__version__ = "1.0"
__license__ = "GPLV3"
__author__ ="Pablo ALINGERY"
__credit__=["Pablo ALINGERY", "Elie SOUBRIE"]
__maintainer__="Pablo ALINGERY"
__email__="medoc-contact@ias.u-psud.fr"


from sitools2.core.pySitools2 import *

#sitools2_url='http://medoc-sdo.ias.u-psud.fr'
sitools2_url='http://idoc-solar-portal-test.ias.u-psud.fr'
#sitools2_url='http://localhost:8182'

def media_get(MEDIA_DATA_LIST=[], TARGET_DIR=None, DOWNLOAD_TYPE=None, **kwds) :
	"""Use search result as an entry to call get_file method"""

	for k,v  in kwds.iteritems():
		if k=='target_dir':
			TARGET_DIR=v
		if k=='download_type':
			DOWNLOAD_TYPE=v
		if k=='media_data_list':
			MEDIA_DATA_LIST=v

	if kwds.has_key('media_data_list'):
		del kwds['media_data_list']

	if len(MEDIA_DATA_LIST)==0 :
		sys.stdout.write("Nothing to download\n")
		return(-1)

	if DOWNLOAD_TYPE is None :
		for item in MEDIA_DATA_LIST:
			if item.ias_location!='':
				item.get_file(TARGET_DIR=TARGET_DIR, **kwds)
			else:
				sys.stdout.write("The data for recnum %s is not at IAS \n" % str(item.recnum) )
	else :
		media_get_selection(MEDIA_DATA_LIST=MEDIA_DATA_LIST, TARGET_DIR=TARGET_DIR, DOWNLOAD_TYPE=DOWNLOAD_TYPE, **kwds)
		

def media_get_selection(MEDIA_DATA_LIST=[], DOWNLOAD_TYPE="TAR", **kwds) :
	"""Use __getSelection__ method providing search result as an entry"""

# Define dateset target	
	if sitools2_url=='http://medoc-sdo-test.ias.u-psud.fr' :
		sdo_dataset=Sdo_IAS_SDO_dataset(sitools2_url+"/webs_IAS_SDO_dataset")
	elif sitools2_url=='http://idoc-solar-portal-test.ias.u-psud.fr' and SERIE.startswith('hmi') :
		sdo_dataset=Sdo_IAS_SDO_dataset(sitools2_url+"/webs_hmi_dataset")
	elif sitools2_url=='http://idoc-solar-portal-test.ias.u-psud.fr' and SERIE.startswith('aia') :
		sdo_dataset=Sdo_IAS_SDO_dataset(sitools2_url+"/webs_aia_dataset")

	for k,v  in kwds.iteritems():
		if k=='download_type':
			DOWNLOAD_TYPE=v
		if k=='media_data_list':
			MEDIA_DATA_LIST=v

	if kwds.has_key('media_data_list'):
		del kwds['media_data_list']

	if len(MEDIA_DATA_LIST)==0 :
		sys.stdout.write("Nothing to download\n")
		return(-1)

	media_data_sunum_list=[]
	for item in MEDIA_DATA_LIST:
		if item.ias_location!='':
			media_data_sunum_list.append(item.sunum)
		else :
			sys.stdout.write("The data for recnum %s is not at IAS\n" % str(item.recnum))
	sdo_dataset.__getSelection__(SUNUM_LIST=media_data_sunum_list, DOWNLOAD_TYPE=DOWNLOAD_TYPE, **kwds)

def media_search(DATES=None,WAVES=['94','131','171','193','211','304','335','1600','1700'],SERIE='aia.lev1',CADENCE=['1 min'],NB_RES_MAX=-1,**kwds):
	"""Use the generic search() from pySitools2 library for Sitools2 SDO instance located at IAS
	Parameters available are DATES, WAVES, CADENCE and NB_RES_MAX
	DATES is the interval of dates within you wish to make a research, it must be specifed and composed of 2 datetime elements d1 d2, with d2 >d1
	WAVES is the wavelength (in Angstrom), it must be a list of wave and wave must be in the list ['94','131','171','193','211','304','335','1600','1700']
	if WAVES is not specified WAVES values ['94','131','171','193','211','304','335','1600','1700']
	CADENCE is the cadence with you with to make a research, it must be a string and in list ['12 sec','1 min', '2 min', '10 min', '30 min', '1 h', '2 h', '6 h', '12 h' , '1 day']
	if CADENCE is not specified, CADENCE values '1 min'
	NB_RES_MAX is the nbr of results you wish to display from the results 
	it must be an integer and if specified must be >0
	"""
#Allow lower case entries
	for k,v  in kwds.iteritems():
		if k not in ['dates','waves','cadence','nb_res_max','serie']:
			sys.stdout.write("Error in search():\n'%s' entry for the search function is not allowed" % k)
			return(-1) 
		elif k=='dates':
			DATES=v
		elif k=='waves':
			WAVES=v
		elif k=='cadence':
			CADENCE=v
		elif k=='nb_res_max':
			NB_RES_MAX=v
		elif k=='serie':
			SERIE=v

	sys.stdout.write ("Loading MEDIA Sitools2 client : %s " % sitools2_url)

#Define dataset url
	if sitools2_url.startswith('http://medoc-sdo') :
		sdo_dataset=Sdo_IAS_SDO_dataset(sitools2_url+"/webs_IAS_SDO_dataset")
	elif sitools2_url=='http://idoc-solar-portal-test.ias.u-psud.fr' and SERIE.startswith('hmi') :
		sdo_dataset=Sdo_IAS_SDO_dataset(sitools2_url+"/webs_IAS_SDO_HMI_dataset")
	elif sitools2_url=='http://idoc-solar-portal-test.ias.u-psud.fr' and SERIE.startswith('aia') :
		sdo_dataset=Sdo_IAS_SDO_dataset(sitools2_url+"/webs_IAS_SDO_AIA_dataset")
#	sdo_dataset=Sdo_IAS_SDO_dataset(sitools2_url+"/webs_HMI_SDO_dataset")
#	sdo_dataset=Sdo_IAS_SDO_dataset(sitools2_url+"/webs_hmi_dataset")
	print sdo_dataset

	DATES_OPTIM=[]

######################CONTROL_START
	if DATES is None:
		sys.stdout.write("Error in search():\nDATES entry must be specified")
		return(-1)
	if type(DATES).__name__!='list' :
			mess_err="Error in search():\nentry type for DATES is : %s\nDATES must be a list type" % type(DATES).__name__
			sys.stdout.write(mess_err)
			return(-1)
	if len(DATES)!=2:
		mess_err="Error in search() : %d elements specified for DATES\nDATES param must be specified and a list of 2 elements" %len(DATES)
		sys.stdout.write(mess_err)
		return(-1)
	for date in DATES :
		if type(date).__name__!='datetime' :
			mess_err="Error in search() : type for DATES element is %s \nDATES list element must be a datetime type" % type(date).__name__
			sys.stdout.write(mess_err)
			return(-1)
		else :
#Trick to adapt to date format on solar-portal-test :
			if sitools2_url=='http://idoc-solar-portal-test.ias.u-psud.fr' :
				DATES_OPTIM.append(str(date.strftime("%Y-%m-%dT%H:%M:%S"))+".000")
			else :
				DATES_OPTIM.append(str(date.strftime("%Y-%m-%dT%H:%M:%S")))
	if DATES[1]<= DATES[0]:
		mess_err="Error in search():\nd1=%s\nd2=%s\nfor DATES =[d1,d2] d2 should be > d1" %(DATES[1].strftime("%Y-%m-%dT%H:%M:%S"),DATES[2].strftime("%Y-%m-%dT%H:%M:%S"))
		sys.stdout.write(mess_err)
		return(-1)
	WAVES_allowed_list=['94','131','171','193','211','304','335','1600','1700','6173']
	SERIE_allowed_list=['aia.lev1','hmi.sharp_720s','hmi.sharp_720s_nrt','hmi.m_720s','hmi.sharp_cea_720s_nrt','hmi.ic_720s','hmi.ic_nolimbdark_720s_nrt']
	if type(WAVES).__name__!='list' :
			mess_err="Error in search():\nentry type for WAVES is : %s\nWAVES must be a list type" % type(WAVES).__name__
			sys.stdout.write(mess_err)
			return(-1)
	for wave in WAVES :
		if type(wave).__name__!='str' :
			mess_err="Error in search():\nEntry type for WAVES element is %s\nlist element for WAVES must be a string type" % type(wave).__name__
			sys.stdout.write(mess_err)
			return(-1)
		if wave not in WAVES_allowed_list:
			mess_err="Error in search():\nWAVES= %s not allowed\nWAVES must be in list %s" % (WAVES,WAVES_allowed_list)
			sys.stdout.write(mess_err)
			return(-1)
	CADENCE_allowed_list={'12s':'12 sec' , '1m':'1 min', '2m':'2 min', '10m':'10 min', '30m': '30 min', '1h' :'1 h', '2h':'2 h', '6h': '6 h', '12h':'12 h' , '1d': '1 day'}
	if type(CADENCE).__name__!='list' :
			mess_err="Error in search():\nentry type for CADENCE is : %s\nCADENCE must be a list type" % type(CADENCE).__name__
			sys.stdout.write(mess_err)
			return(-1)
	if len(CADENCE)!=1 :
		mess_err="Error in search():\n%d elements specified for CADENCE\nCADENCE param must be specified and a list of only one element" % len(DATES)
		sys.stdout.write(mess_err)
		return(-1)
	if type(SERIE).__name__!='str' :
			mess_err="Error in search():\nentry type for SERIE is : %s\nSERIE must be a str type" % type(SERIE).__name__
			sys.stdout.write(mess_err)
			return(-1)
	if SERIE not in SERIE_allowed_list  :
			mess_err="Error in search():\nSERIE= %s not allowed\nSERIE must be in list %s" % (SERIE,SERIE_allowed_list)
			sys.stdout.write(mess_err)
			return(-1)
	if SERIE.startswith('hmi'):
			WAVES=['6173']
	for cadence in CADENCE:
		if (cadence not in CADENCE_allowed_list.keys()) and (cadence not in CADENCE_allowed_list.values()) :
			mess_err="Error in search():\nCADENCE= %s not allowed\nCADENCE must be in list %s" % (CADENCE,CADENCE_allowed_list)
			sys.stdout.write(mess_err)
			return(-1)
		elif cadence in CADENCE_allowed_list.values():
			CADENCE=[cadence]
		else :
			CADENCE=[CADENCE_allowed_list[cadence]]
	if type(NB_RES_MAX).__name__!='int' :
			mess_err="Error in search():\nentry type for NB_RES_MAX is : %s\nNB_RES_MAX must be a int type" % type(NB_RES_MAX).__name__
			sys.stdout.write(mess_err)
			return(-1)
	if NB_RES_MAX!=-1 and  NB_RES_MAX<0 :
		mess_err="Error in search():\nNB_RES_MAX= %s not allowed\nNB_RES_MAX must be >0" % NB_RES_MAX
		sys.stdout.write(mess_err)
		return(-1)
#######################CONTROL_END 

#Param
	dates_param=[[sdo_dataset.fields_dict['date__obs']],DATES_OPTIM,'DATE_BETWEEN']
	wave_param=[[sdo_dataset.fields_dict['wavelnth']],WAVES,'IN']
	serie_param=[[sdo_dataset.fields_dict['series_name']],[SERIE],'IN']
	cadence_param=[[sdo_dataset.fields_dict['mask_cadence']],CADENCE,'CADENCE']

#Old Param definition
#	dates_param=[[sdo_dataset.fields_list[4]],DATES_OPTIM,'DATE_BETWEEN']
#	wave_param=[[sdo_dataset.fields_list[5]],WAVES,'IN']
#	serie_param=[[sdo_dataset.fields_list[3]],[SERIE],'IN']
#	cadence_param=[[sdo_dataset.fields_list[10]],CADENCE,'CADENCE']

#OUTPUT get,recnum,sunum,series_name,date__obs,wave,ias_location,exptime,t_rec_index,ias_path
	if SERIE=='aia.lev1':
		output_options=output_options=[sdo_dataset.fields_dict['get'], sdo_dataset.fields_dict['recnum'],sdo_dataset.fields_dict['sunum'],sdo_dataset.fields_dict['series_name'],sdo_dataset.fields_dict['date__obs'],sdo_dataset.fields_dict['wavelnth'],sdo_dataset.fields_dict['ias_location'],sdo_dataset.fields_dict['exptime'],sdo_dataset.fields_dict['t_rec_index'], sdo_dataset.fields_dict['ias_path'] ]
	elif SERIE.startswith('hmi.sharp'):
		output_options=[sdo_dataset.fields_dict['recnum'],sdo_dataset.fields_dict['sunum'],sdo_dataset.fields_dict['series_name'],sdo_dataset.fields_dict['date__obs'],sdo_dataset.fields_dict['wavelnth'],sdo_dataset.fields_dict['ias_location'],sdo_dataset.fields_dict['exptime'],sdo_dataset.fields_dict['t_rec_index'], sdo_dataset.fields_dict['ias_path'], sdo_dataset.fields_dict['harpnum'] ]
	elif SERIE.startswith('hmi'):
		output_options=[sdo_dataset.fields_dict['recnum'],sdo_dataset.fields_dict['sunum'],sdo_dataset.fields_dict['series_name'],sdo_dataset.fields_dict['date__obs'],sdo_dataset.fields_dict['wavelnth'],sdo_dataset.fields_dict['ias_location'],sdo_dataset.fields_dict['exptime'],sdo_dataset.fields_dict['t_rec_index'], sdo_dataset.fields_dict['ias_path'] ]

#Sort date_obs ASC, wave ASC
	sort_options=[[sdo_dataset.fields_dict['date__obs'],'ASC'],[sdo_dataset.fields_dict['wavelnth'],'ASC']]
	Q1=Query(dates_param)
	Q2=Query(wave_param)
	Q3=Query(cadence_param)
	Q4=Query(serie_param)
#print Q1
#	print Q2
#	print Q3
#	print Q4


	query_list=[Q1,Q2,Q3,Q4]

	result=sdo_dataset.search(query_list,output_options,sort_options,limit_to_nb_res_max=NB_RES_MAX)
	sdo_data_list=[]
	if len(result) !=0 :
		for i, data in enumerate(result) :
			sdo_data_list.append(Sdo_data(data))
	print "%s results returned" % len(sdo_data_list)
	return sdo_data_list


def media_metadata_search(KEYWORDS=[], RECNUM_LIST=[],SERIE='aia.lev1', **kwds):
		"""Use search() results (the field recnum) in order to provide metadata information from the dataset webs_aia_dataset
		KEYWORDS is the list of names of metadata that you wish to have in the output THAT MUST BE SPECIFIED 
		RECNUM_LIST list of recnum result of media data search
		"""

#		sys.stdout.write("Keywords list is : %s \n" % KEYWORDS)
#		sys.stdout.write("Recnum list is : %s \n" % RECNUM_LIST)
#		sys.stdout.write("Serie is : %s \n" % SERIE)

		#Allow lower case entries
		for k,v  in kwds.iteritems():
			if k not in ['keywords','recnum_list','serie']:
				sys.stdout.write("Error media_metatada_search():\n'%s' entry for the search function is not allowed" % k) 
			elif k=='keywords':
				KEYWORDS=v
			elif k=='recnum_list':
				RECNUM_LIST=v
			elif k=='serie' :
				SERIE=v

#Controls 
		if len(KEYWORDS)==0 :
			sys.stdout.write("Error media_metadata_search():\nkeywords must be specified")
			return(-1)
		if type(KEYWORDS).__name__!='list' :
			mess_err="Error in media_metadata_search():\nentry type for KEYWORDS is : %s\nKEYWORDS must be a list type" % type(KEYWORDS).__name__
			sys.stdout.write(mess_err)
			return(-1)
		if len(RECNUM_LIST)==0 :
			mess_err="Error in media_metadata_search():\nNo recnum_list provided\nPlease check your request" 
			sys.stdout.write(mess_err)
			return(-1)

#Define dataset target 
		if sitools2_url.startswith('http://medoc-sdo') :
			metadata_ds=Sdo_aia_dataset(sitools2_url+"/webs_aia_dataset")

		elif sitools2_url=='http://idoc-solar-portal-test.ias.u-psud.fr' and SERIE=='aia.lev1' :
			metadata_ds=Sdo_aia_dataset(sitools2_url+"/webs_"+"aia_dataset")
		
		elif sitools2_url=='http://idoc-solar-portal-test.ias.u-psud.fr' and SERIE.startswith('hmi') :
			metadata_ds=Sdo_aia_dataset(sitools2_url+"/webs_"+SERIE+"_dataset")
#coquille
#			metadata_ds=Sdo_aia_dataset(sitools2_url+"/"+SERIE+"")

		sys.stdout.write("Dataset is : %s uri : %s \n" % (metadata_ds.name,metadata_ds.uri))

		O1_aia=[]
		for key in KEYWORDS :
			if metadata_ds.fields_dict.has_key(key):
				O1_aia.append(metadata_ds.fields_dict[key])
			else :
				sys.stdout.write("Error metadata_search(): %s keyword does not exist" % key)
				return(-1)
		S1_aia=[[metadata_ds.fields_dict['date__obs'],'ASC']]#sort by date_obs ascendant

		#initialize recnumlist				
		recnumlist=[]
		result=[]
		i=0
# Make a request for each 500 recnum
		if len(RECNUM_LIST)>500 :
			while i< len(RECNUM_LIST) :
#				print i
				recnumlist=RECNUM_LIST[i:i+499]
				recnumlist=map(str,recnumlist)
				param_query_aia=[[metadata_ds.fields_dict['recnum']],recnumlist,'IN']
				Q_aia=Query(param_query_aia)
				result+=metadata_ds.search([Q_aia],O1_aia,S1_aia)
				i=i+499
#				print "taille result : ",len(result)
		else :
			recnumlist=map(str,RECNUM_LIST)
			param_query_aia=[[metadata_ds.fields_dict['recnum']],recnumlist,'IN']
			Q_aia=Query(param_query_aia)
			result+=metadata_ds.search([Q_aia],O1_aia,S1_aia)
		return result



def metadata_info(SERIE='aia.lev1'):
	"""Displays information concerning the metadata dataset webs_aia_dataset 
	For example if you need the list of the fields in aia_dataset use it  
	"""

	#Define dataset url
	if sitools2_url=='http://medoc-sdo-test.ias.u-psud.fr' :
		metadata_ds=Sdo_IAS_SDO_dataset(sitools2_url+"/webs_aia_dataset")
	elif sitools2_url=='http://idoc-solar-portal-test.ias.u-psud.fr' :
		metadata_ds=Sdo_IAS_SDO_dataset(sitools2_url+"/webs_"+SERIE+"_dataset")

	return metadata_ds.display()

def singleton(class_def):
    instances = {}
    def get_instance(Class_heritage):
        if class_def not in instances:
            instances[class_def] = class_def(Class_heritage)
        return instances[class_def]
    return get_instance

#This following classes will only have one instance 
@singleton
class Sdo_aia_dataset(Dataset):
	"""Definition de la classe Sdo_aia_dataset that heritates of Dataset"""

	def __init__(self,url):
		Dataset.__init__(self,url)

#This following classes will only have one instance 
@singleton
class Sdo_IAS_SDO_dataset(Dataset):
	"""Definition de la classe Sdo_IAS_SDO_dataset that heritates of Dataset"""

	def __init__(self,url):
		Dataset.__init__(self,url)

	def __getSelection__(self, SUNUM_LIST=[], FILENAME=None, TARGET_DIR=None, DOWNLOAD_TYPE="TAR",QUIET=False, **kwds) :
		"""Use get_selection to retrieve a tar ball or a zip collection providing a list of sunum  
		"""
		if DOWNLOAD_TYPE.upper() not in ['TAR','ZIP']:
				sys.stdout.write("Error get_selection(): %s type not allowed\nOnly TAR or ZIP is allowed for parameter DOWNLOAD_TYPE" % DOWNLOAD_TYPE  )

		for k,v  in kwds.iteritems():
			if k not in ['filename','target_dir','quiet','download_type']:
				sys.stdout.write("Error get_file():\n'%s' entry for the search function is not allowed" % k) 
			elif k=='filename':
				FILENAME=v
			elif k=='target_dir':
				TARGET_DIR=v
			elif k=='download_type':
				DOWNLOAD_TYPE=v
			elif k=='quiet':
				QUIET=v
		if FILENAME is None :
			FILENAME="IAS_SDO_export_"+datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%S")+"."+DOWNLOAD_TYPE.lower() #if not specified this is the default name
		if TARGET_DIR is not None:
			if not os.path.isdir(TARGET_DIR) :
				print "Error get_file():\n'%s' directory did not exist.\nCreation directory in progress ..." % TARGET_DIR
				os.mkdir(TARGET_DIR)
			if TARGET_DIR[-1].isalnum():
				FILENAME=TARGET_DIR+'/'+FILENAME
			elif TARGET_DIR[-1]=='/':
				FILENAME=TARGET_DIR+FILENAME
			else :
				sys.stdout.write("Error get_file():\nCheck the param TARGET_DIR, special char %s at the end of TARGET_DIR is not allowed." % TARGET_DIR[-1])

		if DOWNLOAD_TYPE.upper()== "TAR":
			plugin_id="plugin02"
		else :
			plugin_id="plugin03"
		if not QUIET :
			print "Download %s file in progress ..." % DOWNLOAD_TYPE.lower()		
	#	Dataset.execute_plugin(self,plugin_name=plugin_id, pkey_list=SUNUM_LIST, FILENAME=FILENAME)
		try :
			Dataset.execute_plugin(self,plugin_name=plugin_id, pkey_list=SUNUM_LIST, FILENAME=FILENAME)
		except :
			print "Error downloading selection %s " % FILENAME
		else :
			if not QUIET :
				print "Download selection %s completed" % FILENAME


		
class Sdo_data():
	"""Definition de la classe Sdo_data """

	def __init__(self,data):
		self.url=''
		self.recnum=0
		self.sunum=0
		self.date_obs=''
		self.series_name=''
		self.wave=0
		self.ias_location=''
		self.ias_path=''
		self.exptime=0
		self.t_rec_index=0
		self.harpnum=0
		self.compute_attributes(data)

	def compute_attributes(self, data) :
		if data.has_key('get'):
			self.url=data['get']
		elif data.has_key('ias_path'):
			self.url=data['ias_path']
		else :
			self.url=''
		self.recnum=data['recnum']
		self.sunum=data['sunum']
		self.date_obs=data['date__obs']
		if data.has_key('series_name'):
			self.series_name=data['series_name']
		else :
			self.series_name=''

		self.wave=data['wavelnth']
		if data.has_key('ias_location'):
			self.ias_location=data['ias_location']
		else :
			self.ias_location=''
		if data.has_key('ias_path'):
			self.ias_path=data['ias_path']
		else :
			self.ias_path=''
		if data.has_key('exptime'):
			self.exptime=data['exptime']
		else :
			self.exptime=0
		self.t_rec_index=data['t_rec_index']
		if data.has_key('harpnum'):
			self.harpnum=data['harpnum']
		else :
			self.harpnum=0
			

	def display(self):
		print self.__repr__()

        def __repr__(self):
	    if  (self.series_name).startswith('hmi.sharp'):
		    return ("url : %s,recnum : %d, sunum : %d, series_name : %s, date_obs : %s, wave : %d, ias_location : %s, exptime : %s, t_rec_index : %d, harpnum : %d\n" %(self.url,self.recnum,self.sunum,self.series_name,self.date_obs,self.wave,self.ias_location,self.exptime,self.t_rec_index,self.harpnum))
	    else:
		    return ("url : %s,recnum : %d, sunum : %d, series_name : %s, date_obs : %s, wave : %d, ias_location : %s, exptime : %s, t_rec_index : %d, ias_path : %s\n" %(self.url,self.recnum,self.sunum,self.series_name,self.date_obs,self.wave,self.ias_location,self.exptime,self.t_rec_index, self.ias_path))

	def get_file(self, DECOMPRESS=False, FILENAME=None, TARGET_DIR=None, QUIET=False, SEGMENT=None, **kwds ):
		"""This method is used to retrieve the data on the client side 
		   DECOMPRESS is set by default to False so compressed file are downloaded, to get uncompressed files set DECOMPRESS=True
		   FILENAME is by design aia.lev1.waveA_date_obs.image_lev1.fits you can change it providing a FILENAME  
		   TARGET_DIR the path of the targetted directory, by design the files are downloaded in the current dir
		   QUIET output active or not, by design the output is active , for a quiet get_file process set QUIET=True 
		"""

#Allow lower case entries
		for k,v  in kwds.iteritems():
			if k not in ['decompress','filename','target_dir','quiet']:
				sys.stdout.write("Error get_file():\n'%s' entry for the search function is not allowed" % k) 
				return(-1)
			elif k=='decompress':
				DECOMPRESS=v
			elif k=='filename':
				FILENAME=v
			elif k=='target_dir':
				TARGET_DIR=v
			elif k=='quiet':
				QUIET=v
		list_files=[]
		filename_pre=""

#Define filename if not provided 
		if FILENAME is None and self.series_name=='aia.lev1':
			filename_pre=self.series_name+"_"+str(self.wave)+"A_"+self.date_obs.strftime('%Y-%m-%dT%H-%M-%S.') #if not specified this is the default name
		
		elif FILENAME is None and (self.series_name).startswith('hmi.sharp') :
			filename_pre=self.series_name+"_"+str(self.wave)+"A_"+self.date_obs.strftime('%Y-%m-%dT%H-%M-%S_')+str(self.harpnum)+"."
		#Check for Ic_720s data 
		elif FILENAME is None and (self.series_name).startswith('hmi') :
			filename_pre=self.series_name+"_"+str(self.wave)+"A_"+self.date_obs.strftime('%Y-%m-%dT%H-%M-%S.')
		elif FILENAME is not None :
			sys.stdout.write("FILENAME defined by user : %s" % FILENAME)
			filename_pre=FILENAME

#Define SEGMENT if it does not exist 
		if SEGMENT is None and self.series_name=='aia.lev1' :
			list_files=['image_lev1']
		elif SEGMENT is None and (self.series_name).startswith('hmi.sharp') :
			list_files=['bitmap','Bp_err','Bp','Br_err','Br','Bt_err','Bt','conf_disambig','continuum', 'Dopplergram', 'magnetogram']
		elif SEGMENT is None and (self.series_name).startswith('hmi.ic') :
			list_files=['continuum']
		elif SEGMENT is None and (self.series_name).startswith('hmi.m') :
			list_files=['magnetogram']
		elif SEGMENT is not None :
			list_files=SEGMENT

#Create target location if it does not exist 
		if TARGET_DIR is not None:
			if not os.path.isdir(TARGET_DIR) :
				print "Error get_file():\n'%s' directory did not exist.\nCreation directory in progress ..." % TARGET_DIR
				os.mkdir(TARGET_DIR)
			if TARGET_DIR[-1].isalnum():
				filename_pre=TARGET_DIR+'/'+filename_pre
			elif TARGET_DIR[-1]=='/':
				filename_pre=TARGET_DIR+filename_pre
			else :
				sys.stdout.write("Error get_file():\nCheck the param TARGET_DIR, special char %s at the end of TARGET_DIR is not allowed." % TARGET_DIR[-1])
				return(-1)

#Specification for aia.lev1 and COMPRESS param 
		if not DECOMPRESS and self.series_name=='aia.lev1':
			self.url=self.url+";compress=rice"
		
#Define filename_path and file_url
		for file_suff in list_files :
			filename_path=filename_pre+file_suff+'.fits'
			if (self.series_name).startswith('hmi') :
			#	filename_path=filename_pre+file_suff+'.fits'
			#	print "filename_path :", filename_path
				file_url=self.url+"/"+file_suff+'.fits'
			#	file_url=self.url+"/"+file_suff+'.fits'
			#	print "filename_url :", file_url
			elif self.series_name==('aia.lev1') :
			#	filename_path=filename_pre+file_suff+'.fits'
			#	print "filename_path :", filename_path
				file_url=self.url
			#	print "filename_url :", file_url
#Retrieve data 
			try :	
				urllib.urlretrieve(file_url, filename_path)
			except :
				print "Error downloading %s " % filename_path
			else :
				if not QUIET :
					print "Download file %s completed" % filename_path

	def metadata_search(self, KEYWORDS=[], **kwds):
		"""Use search() results (the field recnum) in order to provide metadata information from the dataset webs_aia_dataset
		KEYWORDS is the list of names of metadata that you wish to have in the output THAT MUST BE SPECIFIED 
		RECNUM_LIST by designed values self.recnum 
		"""
#Allow lower case entries
		for k,v  in kwds.iteritems():
			if k not in ['keywords','recnum_list']:
				sys.stdout.write("Error get_file():\n'%s' entry for the search function is not allowed" % k) 
				return(-1)
			elif k=='keywords':
				KEYWORDS=v
			elif k=='recnum_list':
				RECNUM_LIST=v

		if len(KEYWORDS)==0 :
			sys.stdout.write("Error metadata_search():\nkeywords must be specified")
			return(-1)
		if type(KEYWORDS).__name__!='list' :
			mess_err="Error in metadata_search():\nentry type for KEYWORDS is : %s\nKEYWORDS must be a list type" % type(KEYWORDS).__name__
			sys.stdout.write(mess_err)
			return(-1)
		if sitools2_url=='http://medoc-sdo.ias.u-psud.fr' :
			metadata_ds=Sdo_aia_dataset(sitools2_url+"/webs_aia_dataset")
		elif sitools2_url=='http://idoc-solar-portal-test.ias.u-psud.fr' :
			metadata_ds=Sdo_aia_dataset(sitools2_url+"/webs_"+self.series_name+"dataset")

		RECNUM_LIST=[str(self.recnum)]
		param_query_aia=[[metadata_ds.fields_dict['recnum']],RECNUM_LIST,'IN']
		Q_aia=Query(param_query_aia)
		O1_aia=[]
		for key in KEYWORDS :
			if metadata_ds.fields_dict.has_key(key):
				O1_aia.append(metadata_ds.fields_dict[key])
			else :
				sys.stdout.write("Error metadata_search(): %s keyword does not exist" % key)
		S1_aia=[[metadata_ds.fields_dict['date_obs'],'ASC']]#sort by date_obs ascendant
		return metadata_ds.search([Q_aia],O1_aia,S1_aia)[0]


def main():
	d1=datetime(2016,6,10,0,0,0)
	d2=d1+timedelta(days=1)
	#sdo_data_list=media_search(DATES=[d1,d2],waves=['335'],cadence=['1h'],nb_res_max=10) 
#	print sdo_data_list
	sdo_data_list=media_search(DATES=[d1,d2],serie='hmi.sharp_cea_720s_nrt',cadence=['1h'],nb_res_max=10) 
	print sdo_data_list
# Unit test media_metadata_search
	print "Test media_metadata_search"
	recnum_list = []
	for item in sdo_data_list :
		recnum_list.append(str(item.recnum))
	print recnum_list
	meta=media_metadata_search(KEYWORDS=['recnum','sunum','date__obs','quality','cdelt1','cdelt2','crval1'], SERIE="hmi.sharp_cea_720s_nrt", RECNUM_LIST=recnum_list)
	print meta

#Unit test get_file
#	for data in sdo_data_list :
#	for data in sdo_hmi_data_list :
#		data.get_file(target_dir='results', SEGMENT=['Br'])

#Unit test metadata_search
#	print "Test metadata_search"
#	for item in sdo_data_list:
#		my_meta_search=item.metadata_search(keywords=['sunum','recnum','quality','cdelt1','cdelt2','crval1'])
#		print my_meta_search
if __name__ == "__main__":
	main()
