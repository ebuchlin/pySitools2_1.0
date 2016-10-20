#! /usr/bin/python
"""
This script has been designed to give python programmers an easy way to interrogate medoc gaia-dem sitools2 interface.
You can make a search providing a date range and get your selection very easilly.
@author: Pablo ALINGERY for IAS 07-03-2013
"""
__version__ = "1.0"
__license__ = "GPL"
__author__ ="Pablo ALINGERY"
__credit__=["Pablo ALINGERY"]
__maintainer__="Pablo ALINGERY"
__email__="pablo.alingery.ias.u-psud.fr,pablo.alingery@exelisvis.com"


from sitools2.core.pySitools2 import *

#sitools2_url='http://medoc-dem.ias.u-psud.fr'
sitools2_url='http://idoc-solar-portal-test.ias.u-psud.fr'

def gaia_get(GAIA_LIST=[], TARGET_DIR=None, DOWNLOAD_TYPE=None, TYPE=None, **kwds) :
	"""Use search result as an entry to call get_file method"""
	kwds=kwds
	if DOWNLOAD_TYPE is not None :
#TYPE is ignored
		get_selection(GAIA_LIST=GAIA_LIST, TARGET_DIR=TARGET_DIR, DOWNLOAD_TYPE=DOWNLOAD_TYPE, **kwds)
	else: 
		for item in GAIA_LIST:
			item.get_file(TARGET_DIR=TARGET_DIR, **kwds)	


def get_selection(GAIA_LIST=[], DOWNLOAD_TYPE="TAR", **kwds) :
	"""Uses the  __getSelection__() method of Sdo_IAS_gaia_dataset classe for Sitools2 GAIA instance located at IAS
	Parameters available are GAIA_LIST and DOWNLOAD_TYPE
	GAIA_LIST is the result list of the following search function 
	DOWNLOAD_TYPE specify the kind of download type of the file expected (tar,zip, tar.gz) 
	PS : Only tar for the moment 
	"""

	gaia_dataset=Sdo_IAS_gaia_dataset(sitools2_url+"/ws_SDO_DEM")
	gaia_data_sunum_list=[]
	for item in GAIA_LIST:
		gaia_data_sunum_list.append(item.sunum_193)
	
	gaia_dataset.__getSelection__(SUNUM_LIST=gaia_data_sunum_list, DOWNLOAD_TYPE=DOWNLOAD_TYPE, **kwds)

def gaia_search(DATES=None,NB_RES_MAX=-1,**kwds):
	"""Uses the generic search() from pySitools2 library for Sitools2 GAIA instance located at IAS
	Parameters available are DATES and NB_RES_MAX
	DATES is the interval of dates within you wish to make a research, it must be specifed and composed of 2 datetime elements d1 d2, with d2 >d1
	NB_RES_MAX is the nbr of results you wish to display from the results 
	it must be an integer and if specified must be >0
	"""
#Allow lower case entries
	for k,v  in kwds.iteritems():
		if k not in ['dates','nb_res_max']:
			sys.exit("Error in search():\n'%s' entry for the search function is not allowed" % k) 
		elif k=='dates':
			DATES=v
		elif k=='nb_res_max':
			NB_RES_MAX=v

	print "Loading GAIA-DEM Sitools2 client : ",sitools2_url
	if sitools2_url.startswith('http://medoc-dem') :
		gaia_dataset=Sdo_IAS_gaia_dataset(sitools2_url+"/ws_SDO_DEM")
	elif sitools2_url.startswith('http://idoc-solar-portal') :
		gaia_dataset=Sdo_IAS_gaia_dataset(sitools2_url+"/webs_GAIA-DEM_dataset")
	elif sitools2_url.startswith('http://localhost'):
		gaia_dataset=Sdo_IAS_gaia_dataset(sitools2_url+"/webs_GAIA-DEM-dataset")
	print gaia_dataset
	DATES_OPTIM=[]
	if DATES is None:
		sys.exit("Error in search():\nDATES entry must be specified")
	if type(DATES).__name__!='list' :
			mess_err="Error in search():\nentry type for DATES is : %s\nDATES must be a list type" % type(DATES).__name__
			sys.exit(mess_err)
	if len(DATES)!=2:
		mess_err="Error in search() : %d elements specified for DATES\nDATES param must be specified and a list of 2 elements" %len(DATES)
		sys.exit(mess_err)
	for date in DATES :
		if type(date).__name__!='datetime' :
			mess_err="Error in search() : type for DATES element is %s \nDATES list element must be a datetime type" % type(date).__name__
			sys.exit(mess_err)
		elif sitools2_url.startswith('http://medoc-sdo') :
			DATES_OPTIM.append(str(date.strftime("%Y-%m-%dT%H:%M:%S")))
		elif sitools2_url.startswith('http://idoc-solar-portal') :
			DATES_OPTIM.append(str(date.strftime("%Y-%m-%dT%H:%M:%S"))+".000")
	if DATES[1]<= DATES[0]:
		mess_err="Error in search():\nd1=%s\nd2=%s\nfor DATES =[d1,d2] d2 should be > d1" %(DATES[1].strftime("%Y-%m-%dT%H:%M:%S"),DATES[2].strftime("%Y-%m-%dT%H:%M:%S"))
		sys.exit(mess_err)
	dates_param=[[gaia_dataset.fields_dict['date_obs']],DATES_OPTIM,'DATE_BETWEEN']
	if type(NB_RES_MAX).__name__!='int' :
			mess_err="Error in search():\nentry type for NB_RES_MAX is : %s\nNB_RES_MAX must be a int type" % type(NB_RES_MAX).__name__
			sys.exit(mess_err)
	if NB_RES_MAX!=-1 and  NB_RES_MAX<0 :
		mess_err="Error in search():\nNB_RES_MAX= %s not allowed\nNB_RES_MAX must be >0" % NB_RES_MAX
		sys.exit(mess_err)
#Ask for download,date_obs,sunum_193,filename,temp_fits_rice,em_fits_rice,width_fits_rice,chi2_fits_rice
#	output_options=[gaia_dataset.fields_list[0],gaia_dataset.fields_list[1],gaia_dataset.fields_list[5],gaia_dataset.fields_list[8],gaia_dataset.fields_list[18],gaia_dataset.fields_list[19],\
#	gaia_dataset.fields_list[20],gaia_dataset.fields_list[21]]
	output_options=[gaia_dataset.fields_dict['download'],gaia_dataset.fields_dict['date_obs'],gaia_dataset.fields_dict['sunum_193'],gaia_dataset.fields_dict['filename'],\
	gaia_dataset.fields_dict['temp_fits_rice'],gaia_dataset.fields_dict['em_fits_rice'],gaia_dataset.fields_dict['width_fits_rice'],gaia_dataset.fields_dict['chi2_fits_rice'] ]
#Sort date_obs ASC
#	sort_options=[[gaia_dataset.fields_list[1],'ASC']]
	sort_options=[[gaia_dataset.fields_dict['date_obs'],'ASC']]
	Q1=Query(dates_param)
	query_list=[Q1]
	result=gaia_dataset.search(query_list,output_options,sort_options,limit_to_nb_res_max=NB_RES_MAX)
	gaia_data_list=[]
	if len(result) !=0 :
		for data in result :
			gaia_data_list.append(Gaia_data(data))
	print "%s results returned" % len(gaia_data_list)
	return gaia_data_list

#Define decorator
def singleton(class_def):
    """Define decorator that will modify the class so decorated and only return the same instance of a class """

    instances = {}

    def get_instance(Class_heritage):
        """Define a function that only return an existing instance of a Class from the dictionary instances define above or add a new element to instances"""

        if class_def not in instances:
            instances[class_def] = class_def(Class_heritage)
        return instances[class_def]

    return get_instance

#This following classes will only have one instance 
@singleton
class Sdo_IAS_gaia_dataset(Dataset):
	"""Define  class Sdo_IAS_gaia_dataset that heritates of Dataset"""

	def __init__(self,url):
		Dataset.__init__(self,url)

	def __getSelection__(self, SUNUM_LIST=[], FILENAME=None, TARGET_DIR=None, DOWNLOAD_TYPE="TAR",QUIET=False, **kwds) :
		"""Use getSelection to retrieve a tar ball or a zip collection providing a list of sunum  
		"""
		if DOWNLOAD_TYPE.upper() not in ['TAR']:
				sys.exit("Error get_selection(): %s type not allowed\nOnly TAR is allowed for parameter DOWNLOAD_TYPE" % DOWNLOAD_TYPE  )
		for k,v  in kwds.iteritems():
			if k not in ['filename','target_dir','quiet','download_type']:
				sys.exit("Error __getSelection__():\n'%s' entry for the search function is not allowed" % k) 
			elif k=='filename':
				FILENAME=v
			elif k=='target_dir':
				TARGET_DIR=v
			elif k=='download_type':
				DOWNLOAD_TYPE=v
			elif k=='quiet':
				QUIET=v
		if FILENAME is None :
			FILENAME="IAS_GAIA_export_"+datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")+"."+DOWNLOAD_TYPE.lower() #if not specified this is the default name
		if TARGET_DIR is not None:
			if not os.path.isdir(TARGET_DIR) :
#				sys.exit("Error get_file():\nCheck the parameter TARGET_DIR, '%s' directory does not exist." % TARGET_DIR)
				os.mkdir(TARGET_DIR)
			if TARGET_DIR[-1].isalnum():
				FILENAME=TARGET_DIR+'/'+FILENAME
			elif TARGET_DIR[-1]=='/':
				FILENAME=TARGET_DIR+FILENAME
			else :
				sys.exit("Error get_file():\nCheck the param TARGET_DIR, special char %s at the end of TARGET_DIR is not allowed." % TARGET_DIR[-1])

		if DOWNLOAD_TYPE.upper()== "TAR":
			plugin_id="download_tar_DEM"
		else :
			plugin_id=""
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


		
class Gaia_data():
	"""Definition de la classe Gaia_data """

	def __init__(self,data):
		self.download=''
		self.sunum_193=0
		self.date_obs=''
		self.filename=''
		self.temp_fits_rice_uri=''
		self.em_fits_rice_uri=''
		self.width_fits_rice_uri=''
		self.chi2_fits_rice_uri=''
		self.compute_attributes(data)

	def compute_attributes(self, data) :
		self.download=data['download']
		self.sunum_193=data['sunum_193']
		self.date_obs=data['date_obs']
		self.filename=data['filename']
		self.temp_fits_rice_uri=data['temp_fits_rice']
		self.em_fits_rice_uri=data['em_fits_rice']
		self.width_fits_rice_uri=data['width_fits_rice']
		self.chi2_fits_rice_uri=data['chi2_fits_rice']

	def display(self):
		print self.__repr__()

        def __repr__(self):
            return ("sunum_193 : %d, date_obs : %s, download : %s, filename : %s,\ntemp_fits_rice : %s,\nem_fits_rice : %s,\nwidth_fits_rice : %s,\nchi2_fits_rice : %s\n" %(self.sunum_193,self.date_obs,self.download,self.filename,self.temp_fits_rice_uri,self.em_fits_rice_uri,self.width_fits_rice_uri,self.chi2_fits_rice_uri))

	def get_file(self, FILENAME=None, TARGET_DIR=None, QUIET=False, TYPE=None, **kwds ):
		"""This method is used to retrieve the data on the client side 
		   DECOMPRESS is set by default to False so compressed file are downloaded, to get uncompressed files set DECOMPRESS=True
		   FILENAME is by design aia.lev1.waveA_date_obs.image_lev1.fits you can change it providing a FILENAME  
		   TARGET_DIR the path of the targetted directory, by design the files are downloaded in the current dir
		   QUIET output active or not, by design the output is active , for a quiet get_file process set QUIET=True 
		"""
		url_dict={\
		'temp': self.temp_fits_rice_uri,\
		'em' : self.em_fits_rice_uri,\
		'width' : self.width_fits_rice_uri,\
		'chi2' : self.chi2_fits_rice_uri\
		}
		filename_dict={}
#Allow lower case entries
		for k,v  in kwds.iteritems():
			if k not in ['filename','target_dir','quiet','type']:
				sys.exit("Error get_file():\n'%s' entry for the search function is not allowed\n" % k) 
			elif k=='filename':
				FILENAME=v
			elif k=='target_dir':
				TARGET_DIR=v
			elif k=='quiet':
				QUIET=v
			elif k=='type':
				TYPE=v
		if TYPE is not None and type(TYPE).__name__!='list' :
			sys.exit("Error get_file():\nTYPE should be a list\n") 
		if FILENAME is None and TYPE is None:
#			if not specified this is the default name
				for value in url_dict.values() :
					key=value.split("/")[-1]
					value=sitools2_url+value
					filename_dict[key]=value		
		elif FILENAME is None and TYPE is not None:
			for type_spec in TYPE :
				if type_spec not in url_dict.keys() and type_spec!='all':
					sys.exit("Error get_file():\nTYPE = %s entry for the search function is not allowed\nTYPE value should be in list 'temp','em','width','chi2', 'all'\n" % TYPE) 
				elif type_spec=='all':
					for value in url_dict.values() :
						key=value.split("/")[-1]
						value=sitools2_url+value
						filename_dict[key]=value
				else :
					for type_spec in TYPE :
						key=url_dict[type_spec].split("/")[-1]
						value=sitools2_url+url_dict[type_spec]
						filename_dict[key]=value

		elif FILENAME is not None and TYPE is not None:
				 sys.exit("Warning get_file():\nFILENAME :%s\nTYPE : %s \nFILENAME and TYPE are both specified at the same time\nNot allowed please remove one\n" % (FILENAME,TYPE))

		elif FILENAME is not None and type(FILENAME).__name__!='dict' :
			sys.exit("Error get_file():\nFILENAME should be a dictionary\n") 
		else :
			for k,v in FILENAME.iteritems() :
				if k not in url_dict.keys(): 
					sys.exit("Error get_file():\nTYPE = %s entry for the search function is not allowed\n \
					TYPE value should be in list 'temp','em','width','chi2'\n" % k)
 				else : 
					key=FILENAME[k]
					value=sitools2_url+url_dict[k]
					filename_dict[key]=value
				
		if TARGET_DIR is not None:
			if not os.path.isdir(TARGET_DIR) :
				sys.stdout.write("Error get_file():\n'%s' directory did not exist.\nCreation directory in progress ..." % TARGET_DIR)
				os.mkdir(TARGET_DIR)
			if TARGET_DIR[-1].isalnum():
				TARGET_DIR=TARGET_DIR+'/'
			else :
				sys.stdout.write("Error get_file():\nCheck the param TARGET_DIR, special char %s at the end of TARGET_DIR is not allowed." % TARGET_DIR[-1])

		for (item,url) in filename_dict.iteritems():
			try :	
				urllib.urlretrieve(url, "%s%s" % (TARGET_DIR,item))
			except :
				print "Error downloading %s%s " % (TARGET_DIR,item)
			else :
				if not QUIET :
					print "Download file %s%s completed" % (TARGET_DIR,item)

def main():
	d1=datetime(2012,8,10,0,0,0)
	d2=d1+timedelta(days=1)
	gaia_data_list=search(DATES=[d1,d2],nb_res_max=10) 
	for data in gaia_data_list :
		data.get_file(target_dir='results')

if __name__ == "__main__":
	main()
