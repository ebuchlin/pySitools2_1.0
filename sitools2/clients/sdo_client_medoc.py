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
__credit__=["Jean-Christophe MALAPERT","Pablo ALINGERY", "Elie SOUBRIE"]
__maintainer__="Pablo ALINGERY"
__email__="jean-christophe.malapert@cnes.fr, pablo.alingery.ias.u-psud.fr, pablo.alingery@exelisvis.com"

from sitools2.core.pySitools2 import *
try:
    from datetime import *
except:
    messageError = "Import failed in module pySitools2_idoc :\n\tdatetime module is required\n"
    sys.stderr.write(messageError)
    raise ImportError(messageError)

SITOOLS_URL='http://medoc-sdo.ias.u-psud.fr'
DATASET_NAME = 'webs_IAS_SDO_dataset'

class Cadence(DecoratorQuery):
    """Decorates the query by a text search."""
    __PATTERN_VALUE = "CADENCE|%s|%s"
    __PATTERN_KEY = "p[%s]"

    def __init__(self, query, column, value):
        super(Cadence, self).__init__(query)
        self.__column = column
        self.__value = value

    def _getParameters(self):
        param = self.query._getParameters()
        key = self.__PATTERN_KEY % (str(self._getIndex()))
        val = self.__PATTERN_VALUE % (self.__column, self.__value)
        #self.__column.getColumnAlias()
        param.update({key:val})
        return param
    
    def _getIndex(self):
        index = self.query._getIndex()
        return index+1  

class Sdo_data():

    def __init__(self, data):
        self.__data = data
        
    def getData(self):
        return self.__data
    
    def getItemByName(self, name):
        return self.getData()[name]
    
    def get_file(self, TARGET_DIR='/tmp/', TYPE=['all'], QUIET=False, FILENAME = None, DECOMPRESS=False):
        if not TARGET_DIR[-1] == '/':
            TARGET_DIR = TARGET_DIR + '/'
                      
        colorred = "\033[01;31m{0}\033[00m"
        colorgrn = "\033[1;36m{0}\033[00m"
        colorgrnok="\033[0;32m{0}\033[00m"

        url = self.getData()['get']
        if FILENAME == None:
            FILENAME = "aia.lev1."+str(self.getData()['wavelnth'])+"A_"+self.getData()['date__obs'].strftime('%Y-%m-%dT%H:%M:%S.')+"image_lev1.fits"
            
	if not DECOMPRESS :
            url = url + ";compress=rice"
            
        if not QUIET :
            print colorgrn.format("Downloading file %s%s .... " % (TARGET_DIR,FILENAME)),
        try :
            Util.urlretrieve(url, TARGET_DIR+FILENAME)
        except :
            if not QUIET :
                print colorred.format("error")
            else:
                print "Error downloading %s%s " % (TARGET_DIR,FILENAME)
        else :
            if not QUIET :
                print colorgrnok.format("completed")
        
    def display(self):
        print self.__str__()
        
    def __str__(self):
        display=""
        colorred = "\033[01;31m{0}\033[00m"
        colorgrn = "\033[1;36m{0}\033[00m"        
        display += colorred.format("Record\n---------") + '\n'
        for i,item in enumerate(self.__data):
            if str(self.__data[item]).startswith('/'):
                display += colorgrn.format('\t' + item + ' = ') + SITOOLS_URL + str(self.__data[item]) + '\n'
            else:
                display += colorgrn.format('\t' + item + ' = ') + str(self.__data[item]) + '\n'
        display += '\n\n'        
        return display
        
        
def media_search(DATES = None, WAVES=['94','131','171','193','211','304','335','1600','1700'], CADENCE=['1 min'], NB_RES_MAX=-1, QUIET=False):
    if not QUIET :
	sys.stdout.write( "Loading MEDIA Sitools2 client : %s\n" % SITOOLS_URL)
    sdo_data_list = []
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

    c = dataset.getColumnByColumnAlias('date__obs')   
    search = dataset.getSearch()    
    request = RelativeRequest()    
    request = DateBetween(request, c.getColumnAlias(), str(DATES[0].strftime("%Y-%m-%dT%H:%M:%S")), str(DATES[1].strftime("%Y-%m-%dT%H:%M:%S")))
    request = Cadence(request,'mask_cadence',CADENCE[0])
    request = EnumerateValues(request, 'wavelnth', WAVES)
    request = ColumnToDisplay(request, columnsToDisplay)    
    request = Sorting(request, ['date__obs', 'wavelnth'])
    search.setQueries(request) 
    result = search.execute(limitResMax=NB_RES_MAX)
    for record in result:
        sdo_data_list.append(Sdo_data(record))
    if not QUIET :
	sys.stdout.write( "%s results returned\n" % len(sdo_data_list))
    return sdo_data_list

def media_get(MEDIA_DATA_LIST, TARGET_DIR="/tmp", QUIET=False, DECOMPRESS=False, FILENAME='myresult', DOWNLOAD_TYPE=None):
    if not QUIET :
        print "Download in progress ..."
    if not TARGET_DIR[-1] == '/':
        TARGET_DIR = TARGET_DIR + '/'    
    if DOWNLOAD_TYPE is not None :
	media_get_selection(MEDIA_DATA_LIST, TARGET_DIR="/tmp/",FILENAME=FILENAME)
    else:
		for media_data in MEDIA_DATA_LIST:
			media_data.get_file(TARGET_DIR, TYPE, QUIET, DECOMPRESS=DECOMPRESS)


def media_get_selection(MEDIA_DATA_LIST, TARGET_DIR="/tmp/", FILENAME='myresult', QUIET=False):
    if not TARGET_DIR[-1] == '/':
        TARGET_DIR = TARGET_DIR + '/'    
    filenames = []
    for media in MEDIA_DATA_LIST:
        filenames.append(media.getItemByName('get'))
    
    dataset = DataSet(SITOOLS_URL, datasetName=DATASET_NAME)
    search = dataset.getSearch()
    request = RelativeRequest()    
    request = EnumerateValues(request,'get', filenames)
    search.setQueries(request)
    result = search.download(TARGET_DIR+FILENAME)
    if not QUIET :
        print result + " is downloaded"         

''' 
def download(DATES, TARGET_DIR="/tmp/", FILENAME='toto'):
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
'''

if __name__ == "__main__":
    request = RelativeRequest()
    request = Cadence(request, 'colA', '2min')
    print (request.getUrl())
