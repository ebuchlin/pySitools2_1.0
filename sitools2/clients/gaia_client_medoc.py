#! /usr/bin/python
"""
This script has been designed to give python programmers an easy way to interrogate medoc gaia-dem sitools2 interface.
You can make a search providing a date range and get your selection very easilly.
@author: Pablo ALINGERY for IAS 07-03-2013
"""
__version__ = "1.0"
__license__ = "GPL"
__author__ = "Pablo ALINGERY"
__credit__ = ["Pablo ALINGERY"]
__maintainer__ = "Pablo ALINGERY"
__email__ = "pablo.alingery.ias.u-psud.fr"

from sitools2.core.pySitools2 import *
from future.utils import iteritems
from future.moves.urllib.request import urlretrieve

#sitools2_url='http://medoc-dem.ias.u-psud.fr'
sitools2_url = 'http://idoc-medoc-test.ias.u-psud.fr'


def gaia_get(gaia_list=[],
             target_dir=None,
             download_type=None,
             type=None,
             **kwds):
    """Donwload gaia dem data from MEDOC server 

    Parameters
    ------------
    gaia_list : list of gaia_data objects
        The result of gaia_search can be passed as an argument of that function.
        The size of the list must be >0
        Ex :
            gaia_data_list = gaia_search(dates=[d1,d2], nb_res_max=10)
            gaia_get(gaia_list=gaia_data_list)
    target_dir : text 
        User can specify the directory of download
        Ex :
            gaia_get(gaia_list=gaia_data_list, target_dir='results')
    download_type : text
        Can be 'TAR' or 'ZIP' 
        Ex :
            gaia_get(gaia_list=gaia_data_list,download_type="tar")

    Returns 
    --------------
    Files located in the target_dir directory 
    """
    kwds = kwds

    allowed_params = [
        'GAIA_LIST', 'TARGET_DIR', 'DOWNLOAD_TYPE'
    ]
    for k, v in iteritems(kwds):
        if k not in allowed_params:
            mess_err = "Error in search():\n'%s' entry for the media_get function is not allowed\n" % k
            raise ValueError(mess_err)
        if k == 'TARGET_DIR':
            target_dir = v
        if k == 'DOWNLOAD_TYPE':
            download_type = v
        if k == 'GAIA_LIST':
            gaia_list = v

    if 'GAIA_LIST' in kwds:
        del kwds['GAIA_LIST']  #don't pass it twice

    if len(gaia_list) == 0:
        mess_err = "Nothing to download\n"
        raise ValueError(mess_err)

    if download_type is not None:
        #filetype is ignored
        get_selection(
            gaia_list=gaia_data_list,
            target_dir=target_dir,
            download_type=download_type,
            **kwds)
    else:
        for item in gaia_list:
            item.get_file(target_dir=target_dir, **kwds)


def get_selection(gaia_list=[], download_type="TAR", **kwds):
    """Donwload a selection from MEDOC server tar or zip file  

    Parameters
    ------------
    gaia_list : list of Sdo_data objects
        The result of media_search can be passed as an argument of that function.
        Ex :
            gaia_data_list = gaia_search(dates=[d1,d2], nb_res_max=10)
            get_selection(gaia_list=gaia_data_list,download_type='TAR')
    download_type : text
        Can be 'TAR' or 'ZIP' 
        Ex :
            gaia_get (gaia_list=gaia_data_list,download_type="TAR")
    **kwds can value target_dir for ex 
    target_dir : text 
        User can specify the directory of download
        Ex :
            get_selection(gaia_list=gaia_data_list, target_dir='results',download_type='TAR')
    Returns 
    --------------
    Files located in the current directory 
    """

    gaia_dataset = Sdo_IAS_gaia_dataset(sitools2_url + "/ws_SDO_DEM")
    gaia_data_sunum_list = []
    for item in gaia_list:
        #To be checked
        gaia_data_sunum_list.append(item.sunum_193)

    gaia_dataset.__getSelection__(
        sunum_list=gaia_data_sunum_list, download_type=download_type, **kwds)


def gaia_search(dates=None, nb_res_max=-1, **kwds):
    """Use the gaia_search() from pySitools2 library for Sitools2 SDO instance located at IAS  

    Parameters
    ------------
    dates : datetime 
    Interval of dates within you wish to make a research, it must be specifed and composed of 2 datetime elements d1 d2, with d2 >d1
    
    nb_res_max : integer
    Nbr of results you wish to display from the results 
    Must be an integer and if specified must be >0

    Returns 
    --------------
    gaia_data list 
    """

    #Allow lower case entries
    for k, v in iteritems(kwds):
        if k not in ['DATES', 'NB_RES_MAX']:
            raise ValueError(
                "Error in search():\n'%s' entry for the search function is not allowed"
                % k)
        elif k == 'DATES':
            dates = v
        elif k == 'NB_RES_MAX':
            nb_res_max = v

    sys.stdout.write("Loading GAIA-DEM Sitools2 client : %s \n" % sitools2_url)
    if sitools2_url.startswith('http://medoc-dem'):
        gaia_dataset = Sdo_IAS_gaia_dataset(sitools2_url + "/ws_SDO_DEM")
    elif sitools2_url.startswith('http://idoc-medoc'):
        gaia_dataset = Sdo_IAS_gaia_dataset(sitools2_url +
                                            "/webs_GAIA-DEM_dataset")
    elif sitools2_url.startswith('http://localhost'):
        gaia_dataset = Sdo_IAS_gaia_dataset(sitools2_url +
                                            "/webs_GAIA-DEM-dataset")
#   print(gaia_dataset)
    dates_optim = []
    if dates is None:
        raise ValueError("Error in search():\ndates entry must be specified")
    if type(dates).__name__ != 'list':
        mess_err = "Error in search():\nentry type for dates is : %s\ndates must be a list type" % type(
            dates).__name__
        raise ValueError(mess_err)
    if len(dates) != 2:
        mess_err = "Error in search() : %d elements specified for dates\ndates param must be specified and a list of 2 elements" % len(
            dates)
        raise ValueError(mess_err)
    for date in dates:
        if type(date).__name__ != 'datetime':
            mess_err = "Error in search() : type for dates element is %s \ndates list element must be a datetime type" % type(
                date).__name__
            raise ValueError(mess_err)
        elif sitools2_url.startswith('http://medoc-sdo'):
            dates_optim.append(str(date.strftime("%Y-%m-%dT%H:%M:%S")))
        elif sitools2_url.startswith('http://idoc-medoc'):
            dates_optim.append(
                str(date.strftime("%Y-%m-%dT%H:%M:%S")) + ".000")
    if dates[1] <= dates[0]:
        mess_err = "Error in search():\nd1=%s\nd2=%s\nfor dates =[d1,d2] d2 should be > d1" % (
            dates[1].strftime("%Y-%m-%dT%H:%M:%S"),
            dates[2].strftime("%Y-%m-%dT%H:%M:%S"))
        raise ValueError(mess_err)
    dates_param = [[gaia_dataset.fields_dict['date_obs']], dates_optim,
                   'DATE_BETWEEN']
    if type(nb_res_max).__name__ != 'int':
        mess_err = "Error in search():\nentry type for nb_res_max is : %s\nNB_RES_MAX must be a int type" % type(
            nb_res_max).__name__
        raise ValueError(mess_err)
    if nb_res_max != -1 and nb_res_max < 0:
        mess_err = "Error in search():\nNB_RES_MAX= %s not allowed\nNB_RES_MAX must be >0" % nb_res_max
        raise ValueError(mess_err)
#Ask for download,date_obs,sunum_193,filename,temp_fits_rice,em_fits_rice,width_fits_rice,chi2_fits_rice
#   output_options=[gaia_dataset.fields_list[0],gaia_dataset.fields_list[1],gaia_dataset.fields_list[5],gaia_dataset.fields_list[8],gaia_dataset.fields_list[18],gaia_dataset.fields_list[19],\
#   gaia_dataset.fields_list[20],gaia_dataset.fields_list[21]]
    output_options=[gaia_dataset.fields_dict['download'],gaia_dataset.fields_dict['date_obs'],gaia_dataset.fields_dict['sunum_193'],gaia_dataset.fields_dict['filename'],\
    gaia_dataset.fields_dict['temp_fits_rice'],gaia_dataset.fields_dict['em_fits_rice'],gaia_dataset.fields_dict['width_fits_rice'],gaia_dataset.fields_dict['chi2_fits_rice'] ]
    #Sort date_obs ASC
    #   sort_options=[[gaia_dataset.fields_list[1],'ASC']]
    sort_options = [[gaia_dataset.fields_dict['date_obs'], 'ASC']]
    Q1 = Query(dates_param)
    query_list = [Q1]
    result = gaia_dataset.search(
        query_list,
        output_options,
        sort_options,
        limit_to_nb_res_max=nb_res_max)
    gaia_data_list = []
    if len(result) != 0:
        for data in result:
            gaia_data_list.append(Gaia_data(data))
    sys.stdout.write("%s results returned\n" % len(gaia_data_list))
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

    def __init__(self, url):
        Dataset.__init__(self, url)

    def __getSelection__(self,
                         sunum_list=[],
                         filename=None,
                         target_dir=None,
                         download_type="TAR",
                         quiet=False,
                         **kwds):
        """Use getSelection to retrieve a tar ball or a zip collection providing a list of sunum  
        """
        if download_type.upper() not in ['TAR']:
            raise ValueError(
                "Error get_selection(): %s type not allowed\nOnly TAR is allowed for parameter download_type"
                % download_type)
        for k, v in iteritems(kwds):
            if k not in ['filename', 'target_dir', 'quiet', 'download_type']:
                raise ValueError(
                    "Error __getSelection__():\n'%s' entry for the search function is not allowed"
                    % k)
            elif k == 'filename':
                filename = v
            elif k == 'target_dir':
                target_dir = v
            elif k == 'download_type':
                download_type = v
            elif k == 'quiet':
                quiet = v
        if filename is None:
            filename = "IAS_GAIA_export_" + datetime.utcnow().strftime(
                "%Y-%m-%dT%H:%M:%S") + "." + download_type.lower(
                )  #if not specified this is the default name
        if target_dir is not None:
            if not os.path.isdir(target_dir):
                #               raise ValueError("Error get_file():\nCheck the parameter target_dir, '%s' directory does not exist." % target_dir)
                os.mkdir(target_dir)
            if target_dir[-1].isalnum():
                filename = target_dir + '/' + filename
            elif target_dir[-1] == '/':
                filename = target_dir + filename
            else:
                raise ValueError(
                    "Warning get_file():\nCheck the param target_dir, special char %s at the end of target_dir is not allowed."
                    % target_dir[-1])

        if download_type.upper() == "TAR":
            plugin_id = "download_tar_DEM"
        else:
            plugin_id = ""
        if not quiet:
            sys.stdout.write("Download %s file in progress ...\n" %
                             download_type.lower())

    #   Dataset.execute_plugin(self,plugin_name=plugin_id, pkey_list=sunum_list, filename=filename)
        try:
            Dataset.execute_plugin(
                self,
                plugin_name=plugin_id,
                pkey_list=sunum_list,
                filename=filename)
        except:
            sys.stdout.write("Error downloading selection %s \n" % filename)
        else:
            if not quiet:
                sys.stdout.write("Download selection %s completed\n" %
                                 filename)
                sys.stdout.flush()


class Gaia_data():
    """Definition de la classe Gaia_data """

    def __init__(self, data):
        self.download = ''
        self.sunum_193 = 0
        self.date_obs = ''
        self.filename = ''
        self.temp_fits_rice_uri = ''
        self.em_fits_rice_uri = ''
        self.width_fits_rice_uri = ''
        self.chi2_fits_rice_uri = ''
        self.compute_attributes(data)

    def compute_attributes(self, data):
        self.download = data['download']
        self.sunum_193 = data['sunum_193']
        self.date_obs = data['date_obs']
        self.filename = data['filename']
        self.temp_fits_rice_uri = data['temp_fits_rice']
        self.em_fits_rice_uri = data['em_fits_rice']
        self.width_fits_rice_uri = data['width_fits_rice']
        self.chi2_fits_rice_uri = data['chi2_fits_rice']

    def display(self):
        print(self.__repr__())

    def __repr__(self):
        return (
            "sunum_193 : %d, date_obs : %s, download : %s, filename : %s,\ntemp_fits_rice : %s,\nem_fits_rice : %s,\nwidth_fits_rice : %s,\nchi2_fits_rice : %s\n"
            % (self.sunum_193, self.date_obs, self.download, self.filename,
               self.temp_fits_rice_uri, self.em_fits_rice_uri,
               self.width_fits_rice_uri, self.chi2_fits_rice_uri))

    def get_file(self,
                 filename=None,
                 target_dir=None,
                 quiet=False,
                 filetype=None,
                 **kwds):
        """Use the get_file() to retrieve data from MEDOC server  

        Parameters
        ------------
        filename : text 
        Name of the file , rename the default name using that parameter 
        
        target_dir : text
        The directory in which you will retreive the data
        If it does not exist it will be created

        quiet : boolean
        Do not print info concerning the data downloaded if that is set to 'True'

        filetype : text
        Can be 'temp', 'em', 'width' or 'chi2'
        Type of file downloaded

        Returns 
        --------------
        MEDOC files on your current or targer_dir directory  
        """
        url_dict={\
        'temp': self.temp_fits_rice_uri,\
        'em' : self.em_fits_rice_uri,\
        'width' : self.width_fits_rice_uri,\
        'chi2' : self.chi2_fits_rice_uri\
        }
        filename_dict = {}
        #Allow upper case entries
        for k, v in iteritems(kwds):
            if k not in ['FILENAME', 'TARGET_DIR', 'QUIET', 'TYPE']:
                raise ValueError(
                    "Error get_file():\n'%s' entry for the search function is not allowed\n"
                    % k)
            elif k == 'FILENAME':
                filename = v
            elif k == 'TARGET_DIR':
                target_dir = v
            elif k == 'QUIET':
                quiet = v
            elif k == 'TYPE':
                filetype = v
        if filetype is not None and type(filetype).__name__ != 'list':
            raise ValueError("Error get_file():\nfiletype should be a list\n")
        if filename is None and filetype is None:
            #           if not specified this is the default name
            for value in url_dict.values():
                key = value.split("/")[-1]
                value = sitools2_url + value
                filename_dict[key] = value
        elif filename is None and filetype is not None:
            for type_spec in filetype:
                if type_spec not in url_dict.keys() and type_spec != 'all':
                    raise ValueError(
                        "Error get_file():\nfilename = %s entry for the get function is not allowed\nfiletype value should be in list 'temp','em','width','chi2', 'all'\n"
                        % filetype)
                elif type_spec == 'all':
                    for value in url_dict.values():
                        key = value.split("/")[-1]
                        value = sitools2_url + value
                        filename_dict[key] = value
                else:
                    for type_spec in filetype:
                        key = url_dict[type_spec].split("/")[-1]
                        value = sitools2_url + url_dict[type_spec]
                        filename_dict[key] = value

        elif filename is not None and filetype is not None:
            raise ValueError(
                "Warning get_file():\nfilename :%s\nfiletype : %s \nfilename and filetype are both specified at the same time\nNot allowed please remove one\n"
                % (filename, filetype))

        elif filename is not None and type(filename).__name__ != 'dict':
            raise ValueError(
                "Error get_file():\nfilename should be a dictionary\n")
        else:
            for k, v in iteritems(filename):
                if k not in url_dict.keys():
                    raise ValueError(
                        "Error get_file():\nfiletype = %s entry for the get function is not allowed\nfiletype value should be in list 'temp','em','width','chi2'\n"
                        % k)
                else:
                    key = filename[k]
                    value = sitools2_url + url_dict[k]
                    filename_dict[key] = value

        if target_dir is not None:
            if not os.path.isdir(target_dir):
                sys.stdout.write(
                    "Error get_file():\n'%s' directory did not exist.\nCreation directory in progress ..."
                    % target_dir)
                os.mkdir(target_dir)
            if target_dir[-1].isalnum():
                target_dir = target_dir + '/'
            else:
                sys.stdout.write(
                    "Error get_file():\nCheck the param target_dir, special char %s at the end of target_dir is not allowed."
                    % target_dir[-1])
        else:
            target_dir = ""
        for (item, url) in iteritems(filename_dict):
            try:
                urlretrieve(url, "%s%s" % (target_dir, item))
            except:
                sys.stdout.write("Error downloading %s%s \n" %
                                 (target_dir, item))
            else:
                if not quiet:
                    sys.stdout.write("Download file %s%s completed\n" %
                                     (target_dir, item))
                    sys.stdout.flush()


def main():
    d1 = datetime(2012, 8, 10, 0, 0, 0)
    d2 = d1 + timedelta(days=1)
    gaia_data_list = gaia_search(dates=[d1, d2], nb_res_max=10)
    for data in gaia_data_list:
        data.get_file(target_dir='results')


if __name__ == "__main__":
    main()
