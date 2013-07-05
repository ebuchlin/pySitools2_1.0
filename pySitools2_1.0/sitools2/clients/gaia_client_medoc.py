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

__author__=["Jean-Christophe MALAPERT", "Pablo ALINGERY"]
__date__ ="$30 mai 2013 21:02:05$"
__credit__=["Jean-Christophe MALAPERT","Pablo ALINGERY", ]
__maintainer__="Pablo ALINGERY"
__email__="jean-christophe.malapert@cnes.fr, pablo.alingery.ias.u-psud.fr, pablo.alingery@exelisvis.com"

from sitools2.core.pySitools2 import *

try:
    from datetime import *
except:
    messageError = "Import failed in module pySitools2_idoc :\n\tdatetime module is required\n"
    sys.stderr.write(messageError)
    raise ImportError(messageError)


SITOOLS_URL='http://medoc-dem.ias.u-psud.fr'
DATASET_NAME = 'ws_SDO_DEM'

class Gaia_data():
    def __init__(self, data):
        self.__data = data
        
    def getData(self):
        return self.__data
    
    def getKeys(self):
        return self.__data.keys()
    
    def getItemByName(self, name):
        return self.getData()[name]
    
    def get_file(self, TARGET_DIR='/tmp/', TYPE=['all'], QUIET=False):
        if not TARGET_DIR[-1] == '/':
            TARGET_DIR = TARGET_DIR + '/'
            
        filesAllToDownload = {
        'temp':SITOOLS_URL+self.getData()['temp_fits_rice'],
        'em':SITOOLS_URL+self.getData()['em_fits_rice'],
        'width':SITOOLS_URL+self.getData()['width_fits_rice'],
        'chi2':SITOOLS_URL+self.getData()['chi2_fits_rice']
        }
        filesToDownload = dict()
            
        if TYPE[0] == 'all':
            filesToDownload = filesAllToDownload
        else:
            for typeFile in TYPE:
                filesToDownload[typeFile] = filesAllToDownload[typeFile]            

        colorred = "\033[01;31m{0}\033[00m"
        colorgrn = "\033[1;36m{0}\033[00m"
	colorgrnok="\033[0;32m{0}\033[00m"

	for (item,url) in filesToDownload.iteritems():
            filename = url.split('/')[-1]
            if not QUIET :
                print colorgrn.format("Downloading file %s%s .... " % (TARGET_DIR,filename)),
            try :
                Util.urlretrieve(url, TARGET_DIR+filename)
            except :
                if not QUIET :
                    print colorred.format("error")
                else:
                    print "Error downloading %s%s " % (TARGET_DIR,filename)
            else :
		if not QUIET :
                    print colorgrnok.format("completed")
        
    def display(self):
        print self.__str__()
        
    def __str__(self):
        display = ""
        colorred = "\033[01;31m{0}\033[00m"
        colorgrn = "\033[1;36m{0}\033[00m"        
        display += colorred.format("Record\n---------")+'\n'
        for i,item in enumerate(self.__data):
            if str(self.__data[item]).startswith('/'):
                display += colorgrn.format('\t' + item + ' = ') + SITOOLS_URL + str(self.__data[item])+'\n'
            else:
                display += colorgrn.format('\t' + item + ' = ') + str(self.__data[item])+'\n'
        display += '\n\n'
        return display
        
        
def gaia_search(DATES,NB_RES_MAX=-1):
    gaia_data_list = []
    dataset = DataSet(SITOOLS_URL, datasetName=DATASET_NAME)    
    columnsToDisplay = []
    cs = dataset.getColumns()
    for c in cs:    
        if c.hasColumnRenderer():
            render = c.getColumnRenderer()
            if not render.getBehavior() in ['datasetIconLink','noClientAccess','ImgThumbSQL']:
                columnsToDisplay.append(c.getColumnAlias())
        else:            
            columnsToDisplay.append(c.getColumnAlias())

    c = dataset.getColumnByColumnAlias('date_obs')   
    search = dataset.getSearch()    
    request = RelativeRequest()    
    request = DateBetween(request, c.getColumnAlias(), str(DATES[0].strftime("%Y-%m-%dT%H:%M:%S")), str(DATES[1].strftime("%Y-%m-%dT%H:%M:%S")))
    request = ColumnToDisplay(request, columnsToDisplay)
    request = Sorting(request, ['date_obs'])
    search.setQueries(request) 
    result = search.execute(limitResMax=NB_RES_MAX)
    for record in result:
        gaia_data_list.append(Gaia_data(record))
    return gaia_data_list

def gaia_get(GAIA_LIST, TARGET_DIR="/tmp", TYPE=['all'], QUIET=False, FILENAME='myresult' , DOWNLOAD_TYPE=None):

    if not TARGET_DIR[-1] == '/':
        TARGET_DIR = TARGET_DIR + '/'    
    if DOWNLOAD_TYPE is not None :
	gaia_get_selection(GAIA_LIST, TARGET_DIR="/tmp/",FILENAME=FILENAME)
    else:
	for gaia_data in GAIA_LIST:
		gaia_data.get_file(TARGET_DIR=TARGET_DIR, TYPE=TYPE, QUIET=QUIET)

def gaia_download(DATES, TARGET_DIR="/tmp/", FILENAME='toto'):
    if not TARGET_DIR[-1] == '/':
        TARGET_DIR = TARGET_DIR + '/'    
    dataset = DataSet(SITOOLS_URL, datasetName=DATASET_NAME)    
    columnsToDisplay = []
    cs = dataset.getColumns()
    for c in cs:    
        if c.hasColumnRenderer():
            render = c.getColumnRenderer()
            if not render.getBehavior() in ['datasetIconLink','noClientAccess','ImgThumbSQL']:
                columnsToDisplay.append(c.getColumnAlias())
        else:            
            columnsToDisplay.append(c.getColumnAlias())

    c = dataset.getColumnByColumnAlias('date_obs')   
    search = dataset.getSearch()    
    request = RelativeRequest()    
    request = DateBetween(request, c.getColumnAlias(), str(DATES[0].strftime("%Y-%m-%dT%H:%M:%S")), str(DATES[1].strftime("%Y-%m-%dT%H:%M:%S")))
    request = ColumnToDisplay(request, columnsToDisplay)
    request = Sorting(request, ['date_obs'])
    search.setQueries(request) 
    result = search.download(TARGET_DIR+FILENAME)
    print result + " is downloaded"

def gaia_get_selection(GAIA_LIST, TARGET_DIR="/tmp/", FILENAME='myresult'):
    if not TARGET_DIR[-1] == '/':
        TARGET_DIR = TARGET_DIR + '/'    
    filenames = []
    for gaia in GAIA_LIST:
        filenames.append(gaia.getItemByName('filename'))
    dataset = DataSet(SITOOLS_URL, datasetName=DATASET_NAME)
    search = dataset.getSearch()
    request = RelativeRequest()    
    request = EnumerateValues(request,'filename', filenames)
    search.setQueries(request)
    result = search.download(TARGET_DIR+FILENAME)
    print result + " is downloaded"    
    
    
def main():
    d1=datetime(2012,8,10,0,0,0)
    d2=d1+timedelta(days=1) 
    gaia_data_list=search(DATES=[d1,d2],NB_RES_MAX=10)
    for gaia_data in gaia_data_list:
        gaia_data.display()

    #get(gaia_data_list)
    gaia_get(gaia_data_list, TYPE=['em','temp'], QUIET=False)    
    download(DATES=[d1,d2])

if __name__ == "__main__":
    main()
