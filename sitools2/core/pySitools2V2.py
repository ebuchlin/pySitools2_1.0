# -*- coding: utf-8 -*-

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
This is a generic python Sitools2 tool
pySitools2 tool has been designed to perform all operations available within Sitools2.
The code defines several classes SitoolsInstance, Field, Query, Dataset and Project. 
Example of application : 
A Solar tool to request and retrieve SDO data from IAS (Institut d'Astrophysique Spatiale)
see http://sdo.ias.u-psud.fr/python/sdo_client_idoc.html



@author: Pablo ALINGERY for IAS 28-08-2012 and Jean-Christophe MALAPERT
"""
__author__=["Jean-Christophe MALAPERT", "Pablo ALINGERY"]
__date__ ="$16 mai 2013 03:46:43$"
__credit__=["Jean-Christophe MALAPERT","Pablo ALINGERY", "Elie SOUBRIE"]
__maintainer__="Pablo ALINGERY"
__email__="pablo.alingery.ias.u-psud.fr, pablo.alingery@exelisvis.com"

import sys
import logging
from datetime import *

try :
    import urllib
except:
    messageError = "Import failed in module pySitools2_idoc :\n\turllib module is required\n"
    sys.stderr.write(messageError)
    raise ImportError(messageError)
try :
    import simplejson
except:
    messageError = "Import failed in module pySitools2_idoc :\n\tsimplejson module is required\n"
    sys.stderr.write(messageError)
    raise ImportError(messageError)
try :
	from xml.dom.minidom import parseString
except:
    messageError = "Import failed in module pySitools2_idoc :\n\txml.dom.minidom module is required\n"
    sys.stderr.write(messageError)
    raise ImportError(messageError)

class _Util(object):
    """Utility class"""
    @staticmethod
    def format(name, dataItem, eltsToParse=None):
        """Formats a list to display it.                
        Input Parameters
        ----------------
        name : name of the object that contains a list of afftributes
        dataItem : list of attributes
        eltsToParse : elts to display
        
        Return
        ------
        Returns a string to display
        
        Note : When eltsToParse is no defined then all the list is displayed."""
        display = []
        if eltsToParse == None:
            display = dataItem
        else:
            display = eltsToParse
        
        str = "%s object display:\n"%(name)       
        for key, value in enumerate(display):
            str += "\t%s : %s = %s\n"%(key, value, dataItem[value])
        return str
    
    @staticmethod
    def retrieveJsonResponseFromServer(url):
        """Retrieves a JSON response from the server.
        Input parameters
        ----------------
        url : url to call for retrieving the JSON response
        
        Return
        ------
        A dictionary
        
        Exception
        ---------
        SITools2Exception when a problem during the download or parsing happens"""
        jsonData = None
        try:
            data = urllib.urlopen(url)
            jsonData = simplejson.load(data)
        except Exception as ex:
            raise Sitools2Exception(ex)
        return jsonData
                  

class Sitools2Exception(Exception):
    """SITools2 Exception"""
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)


class _Log(object):
    """Module Logger.
    Create a module logger with the following format '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    """    
    @staticmethod
    def getLogger(name, level = logging.INFO):
        """Returns the logger
        Parameters
        ----------
        name : logger name
        level : logging.level (par default logging.INFO)
            
        Return
        ------
        Returns the logger

        """
        # create logger
        logger = logging.getLogger(name) 
        logger.setLevel(level)
        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(level)
        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # add formatter to ch
        ch.setFormatter(formatter)
        # add ch to logger
        logger.addHandler(ch)
        return logger 

class Sitools2(object):
    """An abstract class providing the SITools2 base URL"""
    
    VERSIONS = ['1.0'] # the compatible versions of this core with SITools2
    
    def __init__(self, baseUrl):
        """Constructs a new instance with the SITools2 base URL."""
        self.__baseUrl = baseUrl
    
    def version(self):
        """Returns the version number."""
        return VERSIONS
    
    def getBaseUrl(self):
        """Returns the SITools2 base URL."""
        return self.__baseUrl
    
class Projects(Sitools2):
    """Stores the server response when calling the list of projects
    from a SITools2 instance that is installed on a host
    
    Projects provides the list of projects that are hosted by SITools2.
    A project can be public or not and contains some information
    
    This is an example on how to use this class
    
    Exception when a problem is detected:
    >>> projects = Projects('http://foo.com')
    Traceback (most recent call last):
        ...
    Sitools2Exception: JSONDecodeError('No JSON object could be decoded: line 1 column 0 (char 0)',)
    
    Now, we use a existing instance:
    >>> projects = Projects('http://medoc-sdo.ias.u-psud.fr')
    
    We can retrieve the list of the projects that the instance hosts:
    >>> projectsList = projects.getProjects()
    
    Computes the number of projects that are hosted
    >>> len(projectsList)
    2
    
    Retrieves the parameter of the constructor
    >>> projects.getBaseUrl()
    'http://medoc-sdo.ias.u-psud.fr'
    """
    PROJECTS_URI = '/sitools/portal/projects'
    
    def __init__(self, baseUrl):
        """Constructs a project by calling a URL."""
        super(Projects, self).__init__(baseUrl)
        self.__logger = _Log.getLogger(self.__class__.__name__)
        self.__projects = []
        self.__parseResponseServer()        
        
    def __parseResponseServer(self):
        """Parses the response of the server.
        Exception
        ---------
        A Sitools2Exception is raised when the server does not send back a success."""
        
        self.__logger.debug(Sitools2.getBaseUrl(self) + Projects.PROJECTS_URI)        
        result = _Util.retrieveJsonResponseFromServer(Sitools2.getBaseUrl(self) + Projects.PROJECTS_URI)
        isSuccess = result['success']
        if isSuccess:            
            data = result['data']
            self.__logger.debug(data)
            for i, dataItem in enumerate(data):
                project = Project(Sitools2.getBaseUrl(self), dataItem)
                self.__projects.append(project)
        else:
            raise Sitools2Exception("Error when loading the server response")                
    
    def getProjects(self):
        """Returns the list of projects that are hosted by baseUrl."""
        return self.__projects
    
    
class Project(Sitools2):
    """Stores the server response when calling a specific project.
    A project provides usefull information about a project such as :
    - project name
    - project description
    - project status providing the availability of the service
    - sitoolsAttachementForUser providing the uri to query to get more information
    - project authorization providing if the current user is authorized to access to the project
    - HTML Description of the project
    - maintenance status
    - maintenance text
    
    Let's start by querying a specific project:
    >>> p = Project('http://medoc-dem.ias.u-psud.fr',projectNameUri='/ws_DEM_projet')
    
    Now we can get its name and other information:
    >>> p.getName()
    'DEM'
    
    >>> p.getDescription()
    'DEM inversion from Chloe Guennou et al.'
    
    >>> p.getImage()
    'http://medoc-dem.ias.u-psud.fr/sitools/common/res/images/DEM_picture_120X120.png'
    
    >>> p.isEnabled()
    True
    
    >>> p.getUri()
    '/ws_DEM_projet'
    
    >>> p.isProtected()
    True
    
    >>> p.getHtmlDescription()
    '<br>'
    
    >>> p.isInMaintenance()
    False
    
    >>> p.getMaintenanceText()
    'Sorry, our DEM database is not accessible at the moment, but it will come back soon!<br>'
    """
    ELEMENTS_TO_PARSE = ['name','description','image','status','sitoolsAttachementForUsers',
                         'authorized','htmlDescription','maintenance','maintenanceText']
    
    def __init__(self, baseUrl, dataItem = None, projectNameUri = None):
        """Constructor.
        Inputs
        ------
        baseUrl : SIToole2 baseURL
        dataItem : response from the server (optional)
        projectNameUri : URI of the project (optional)
        
        Exception
        ---------
        Sitools2Exception is raised when both dataItem and projectNameUri are not None.
        
        Note
        ----
        - dataItem is used in the Projects class. When it is used, an update of dataItem is done
        - projectNameUri is the URI of the project != URI of the project in the portal
        """
        super(Project, self).__init__(baseUrl)
        self.__logger = _Log.getLogger(self.__class__.__name__)
        self.__dataItem = dataItem        
        self.__projectNameUri = projectNameUri
        if dataItem != None and projectNameUri != None:
            raise Sitools2Exception("You cannot set both dataItem and projectNameUri.")
        elif projectNameUri == None:
            self.__logger.debug("updates the project.")
            self.__updateDataItem()
        else:
            self.__logger.debug("parses the project.")
            self.__dataItem = self.__parseResponseServer(projectNameUri)
        
    def __updateDataItem(self):
        """Updates dataItem."""
        uri = self.getUri()        
        self.__dataItem = self.__parseResponseServer(uri)                
    
    def __parseResponseServer(self, uri):
        """Parses the server response.
        Input
        -----
        uri : URI of the project to call
        
        Return
        ------
        Returns the dataItem
        
        Exception
        ---------
        Sitools2Exception when the server response is not a success"""
        
        self.__logger.debug("URL to parse: %s"%(Sitools2.getBaseUrl(self) + uri))
        result = _Util.retrieveJsonResponseFromServer(Sitools2.getBaseUrl(self) + uri)        
        isSuccess = result['success']
        if isSuccess:
            data = result['project']            
            return data
        else:
            raise Sitools2Exception("Error when loading the server response")
        
    
    def getName(self):
        """Returns the project name."""
        return self.__dataItem['name']
    
    def getDescription(self):
        """Returns the project description when available."""
        return self.__getNone(self.__dataItem['description'])
    
    def getImage(self):
        """Returns the project image when available."""
        value = self.__getNone(self.__dataItem['image']['url'])
        if value == None:
            return None
        else:
            return Sitools2.getBaseUrl(self) + self.__dataItem['image']['url']
    
    def isEnabled(self):
        """Returns True when the project is enabled otherwise False."""
        if self.__dataItem['status'] == 'ACTIVE':
            return True
        else:
            return False
   
    def getUri(self):
        """Returns the project URI."""
        return self.__dataItem['sitoolsAttachementForUsers']    
    
    def isProtected(self):
        """Returns True when the web project is protected otherwise False."""
        if self.__dataItem['authorized'] is True:
            return False
        else:
            return True

    def getHtmlDescription(self):
        """Returns the HTML description of the project when available."""
        return self.__getNone(self.__dataItem['htmlDescription'])
    
    def isInMaintenance(self):
        """Returns True when the project is in maintenance otherwise False."""
        if self.__dataItem['maintenance'] is True:
            return True
        else:
            return False
    
    def getMaintenanceText(self):
        """Returns the maintenance text."""
        return self.__getNone(self.__dataItem['maintenanceText'])
    
    def getDataSets(self):
        return Datasets(Sitools2.getBaseUrl(self), self.__dataItem['dataSets'])
    
    def display(self):
        """Displays the object."""
        print self.__repr__
    
    def __getNone(self, val):
        """Returns None when val is empty otherwise val."""
        if val != None and len(val)!=0:
            return val
        else:
            return None
        
    def __repr__(self):        
        return _Util.format(self.__class__.__name__, self.__dataItem, Project.ELEMENTS_TO_PARSE)
            
        

class Datasets(Sitools2):
    """Stores the list of datasets related to a project name.
    This class provides information such as :
    - the number of datasets
    - the list of datasets
    - search by dataset name
    
    Let's start by querying a specific project:
    >>> p = Project('http://medoc-dem.ias.u-psud.fr',projectNameUri='/ws_DEM_projet')
    
    >>> datasets = p.getDataSets()
    
    Now, we can get the number of datasets related to the project ws_DEM_project
    >>> datasets.getCount()
    2
    
    We can get a specific dataset in the list
    >>> dataset = datasets.getDataset(0)
    
    If we try to get a dataset outer the array, we get a SITools2Exception
    >>> dataset = datasets.getDataset(3)
    Traceback (most recent call last):
        ...
    IndexError: list index out of range
    """     
   
    def __init__(self, baseUrl, data):
        """Constructs the list of the datasets
        Inputs
        -----
        baseUrl : SITools2 base URL
        data : the response of the server when a specific project is called.        

        Exception
        ---------
        Sitools2Exception when a dataset cannot be instanciated."""
        
        super(Datasets, self).__init__(baseUrl)
        self.__datasets = []
        for dataset in data:
            self.__datasets.append(DataSet(Sitools2.getBaseUrl(self), dataset))
        
    def getCount(self):
        """Returns the number of datasets."""
        return len(self.__datasets)
    
    def getDatasets(self):
        """Returns the list of Dataset Objects."""
        return self.__datasets
    
    def getDataset(self, index):
        """Returns a specific dataset Object in the list.
        Input
        -----
        index : index number in the list
        
        Return
        ------
        A Dataset Object
        
        Exception
        ---------
        IndexError: list index out of range"""
        return self.__datasets[index]
    
    def getDatasetByName(self, name):
        """Returns a Dataset Object by its name.
        Input
        -----
        name : dataset name to search
        
        Return
        ------
        A Dataset Object
        
        Exception
        ---------
        Sitools2Exception: cannot find the dataset"""
        for dataset in self.__datasets:
            datasetName = dataset.getName()
            if datasetName == name:
                return dataset
        raise Sitools2Exception("cannot find the dataset %s"%(name))
                        
        
class DataSet(Sitools2):
    """Stores a dataset.
    This class provides information such as :
    - the dataset name
    - the dataset description
    - the URI description
    - if the web service is enabled
    - if the dataset is protected for you
    - if the dataset is visible in the web interface
    - the number of records
    - the list of dataset columns/attributes
    - the search capability.
    
    Let's start by querying a specific dataset:
    >>> dataset = DataSet( 'http://medoc-dem.ias.u-psud.fr', datasetName='ws_SDO_DEM')
    
    Now, we can retrieve the number of records in this dataset
    >>> dataset.nbRecords()
    8245
    """
    def __init__(self, baseUrl, dataItem = None, datasetName = None):
        super(DataSet, self).__init__(baseUrl)
        self.__logger = _Log.getLogger(self.__class__.__name__)
        if datasetName == None:
            self.__dataItem = dataItem        
            self.__updateDataItem()
        else:
            self.__dataItem = self.__parseResponseServer('/'+datasetName)        
        self.__countNbRecords()
        
        
    def __updateDataItem(self):
        """Updates dataItem."""
        uri = self.getUri()        
        self.__dataItem = self.__parseResponseServer(uri)
    
    def __countNbRecords(self):
        result = _Util.retrieveJsonResponseFromServer(Sitools2.getBaseUrl(self) + self.getUri() + '/count')
        self.__dataItem['nbrecords'] = result['total']
    
    def __parseResponseServer(self, uri):
        """Parses the server response.
        Input
        -----
        uri : URI of the project to call
        
        Return
        ------
        Returns the dataItem
        
        Exception
        ---------
        Sitools2Exception when the server response is not a success"""
        
        self.__logger.debug("URL to parse: %s"%(Sitools2.getBaseUrl(self) + uri))
        result = _Util.retrieveJsonResponseFromServer(Sitools2.getBaseUrl(self) + uri)        
        isSuccess = result['success']
        if isSuccess:
            data = result['dataset']            
            return data
        else:
            raise Sitools2Exception("Error when loading the server response")
        
    def updateCountNbRecords(self):
        self.__countNbRecords()
        
    def getName(self):
        return self.__dataItem['name']
    
    def getDescription(self):
        return self.__dataItem['description']
    
    def getUri(self):
        if self.__dataItem.has_key('url'):
            return self.__dataItem['url']
        else:
            return self.__dataItem['sitoolsAttachementForUsers']
    
    def isEnabled(self):
        if self.__dataItem['status'] == "ACTIVE":
            return True
        else:
            return False
        
    def isProtected(self):
        if self.__dataItem['authorized'] is True:
            return False
        else:
            return True        
    
    def isVisible(self):
        if self.__dataItem['visible'] is True:
            return True
        else:
            return False
    
    def nbRecords(self):
        return self.__dataItem['nbrecords']
    
    #def getHtmlDescription(self):
    #    desc = None
    #    properties = self.__dataItem['properties']
    #    for key, value in enumerate(properties):
    #        if value["name"] == "descriptionHTML":
    #            desc = value["value"]
    #            break
    #    return desc
    
    #def getImage(self):
    #    image = None
    #    properties = self.__dataItem['properties']
    #    for key, value in enumerate(properties):
    #        if value["name"] == "imageUrl":
    #            image = value["value"]
    #            break
    #    return image
    
    def getColumns(self):
        return Columns(self.__dataItem['columnModel'])
    
    def getSearch(self):
        return Search(self.getColumns(), Sitools2.getBaseUrl(self) + self.getUri())
    
class Columns:
    def __init__(self, data):
        self.__columns = []
        for column in data:
            self.__columns.append(Column(column))
    
    def getCount(self):
        return len(self.__columns)
    
    def getColumns(self):
        return self.__columns
    
    def getColumn(self, index):
        return self.__columns[index]
    
    def getColumnByColumnAlias(self, name):        
        for column in self.__columns:
            columnAlias = column.getColumnAlias()
            if columnAlias == name:
                return column
        raise Sitools2Exception("cannot find the column %s"%(name))


class Column:
    
    def __init__(self, data):
        self.__data = data
    
    def getDataIndex(self):
        return self.__data['dataIndex']
    
    def getHeader(self):
        return self.__data['header']
    
    def isSortable(self):
        return self.__data['sortable']
    
    def isVisible(self):
        return self.__data['visible']
    
    def isFilter(self):
        if self.__data.has_key('filter'):
            return self.__data['filter']
        else:
            return False
    
    def isPrimaryKey(self):
        return self.__data['primaryKey']
    
    def hasColumnRenderer(self):
        return self.__data.has_key('columnRenderer')
    
    def getColumnRenderer(self):        
        return ColumnRender(self.__data['columnRenderer'])
    
    def getColumnAlias(self):
        return self.__data['columnAlias']
    
    def getSqlColumnType(self):
        if self.__data.has_key('sqlColumnType'):
            return self.__data['sqlColumnType']
        else:
            return None       
    
    def getOrderBy(self):
        if self.__data.has_key('orderBy'):
            return self.__data['orderBy']
        else:
            return None         
    
    def getFormat(self):
        if self.__data.has_key('format'):
            return self.__data['format']
        else:
            return None        
   
class ColumnRender:
    
    ENUM_BEHAVIOR = ['localUrl','extUrlNewTab','extUrlDesktop','ImgNoThumb','ImgAutoThumb',
    'ImgThumbSQL', 'datasetLink', 'datasetIconLink','noClientAccess']

    def __init__(self, data):
        self.__data = data
    
    def getBehavior(self):
        return self.__data['behavior']
    
    def getDatasetLinkUrl(self):
        return self.__data['datasetLinkUrl']
    
    def getToolTip(self):
        return self.__data['toolTip']

class Query():
    """Definition of a Query class.
       A Query defines the request passed to the server. 
       It can have the following attributes : fields_list, name_list, operation.
       The parameter operation can value : ge, le, gte, lte, lt, eq, gt, lte, like, in, numeric_between, date_between, cadence (dev for IAS) .
    """

    def __init__(self, columns, value, operation):
        """Constructor."""
        self.__logger = _Log.getLogger(self.__class__.__name__)
        self.__names = []
        for column in columns:
            self.__names.append(column.getColumnAlias())
        self.__values = value
        if operation =='GE' : 
            operation='GTE'
        elif operation == 'LE' : 
            operation='LTE'
        self.__operation = operation
    
    def getNames(self):        
        return self.__names
    
    def getValues(self):
        return self.__values
    
    def getOperation(self):
        return self.__operation    

class Search:
    
    LOGICAL_OPERATORS = ['LT', 'EQ', 'GT', 'LTE', 'GTE']
    
    def __init__(self, columns, url):
        self.__logger = _Log.getLogger(self.__class__.__name__)
        self.__columns = []
        self.__availableFilterCols = []
        self.__availableSortableCols = []
        self.__queryParameters = []
        self.__sortParameters = []
        self.__outputColumns = columns.getColumns()
        self.__url = url
        for column in columns.getColumns():
            if column.isFilter():
                self.__availableFilterCols.append(column)
            if column.isSortable():
                self.__availableSortableCols.append(column)
            if column.hasColumnRenderer():
                columnRender = column.getColumnRenderer()
                behavior = columnRender.getBehavior()
                if behavior != "noClientAccess":
                    self.__columns.append(column)
    
    def getAvailableFilterCols(self):
        return self.__availableFilterCols
    
    def getAvailableSortCols(self):
        return self.__availableSortableCols    
    
    def getColumns(self):
        return self.__columns
    
    def addQuery(self, queryParameter):
        self.__queryParameters.append(queryParameter)
        
    def setQueries(self, queryParameters):
        self.__queryParameters = queryParameters
    
    def getQueries(self):
        return self.__queryParameters
    
    def addSort(self, sortParameter):
        self.__sortParameters.append(sortParameter)
        
    def setSorts(self, sortParameters):
        self.__sortParameters = sortParameters
    
    def getSorts(self):
        return self.__sortParameters    
    
    def setOutputColumns(self, columns):
        self.__outputColumns = columns
    
    def getOutputColumns(self):
        return self.__outputColumns
    
    def getOutputColumn(self, columnAlias):
        result = None
        for column in self.__outputColumns:
            if column.getColumnAlias() == columnAlias:
                result = column
                break
        return result
    
    def __buildFilter(self, kwargs):
        for query in self.getQueries():
            j=0#filter counter
            i=0#p counter 
            operation = query.getOperation()
            if operation in ['LT', 'EQ', 'GT', 'LTE', 'GTE'] :
                kwargs.update({
                    'filter['+str(j)+'][columnAlias]' : ",".join(query.getNames()),
                    'filter['+str(j)+'][data][type]' : 'numeric',
                    'filter['+str(j)+'][data][value]' : "|".join(query.getValues()),
                    'filter['+str(j)+'][data][comparison]' : query.getOperation()
                })
                j+=1 #increment filter counter    
            elif operation in ['LIKE'] :
                operation='TEXT'
                i+=1#increment p counter
            elif operation in ['IN'] :
                operation='LISTBOXMULTIPLE'
                kwargs.update({
                    'p['+str(i)+']' : operation+"|"+"|".join(query.getNames())+"|"+"|".join(query.getValues())
                })
                i+=1#increment p counter
            elif operation in ['DATE_BETWEEN','NUMERIC_BETWEEN', 'CADENCE'] :
                kwargs.update({
                    'p['+str(i)+']' : operation+"|"+"|".join(query.getNames())+"|"+"|".join(query.getValues())
                })
                i+=1#increment p counter
            else :
                allowed_operations="ge, le, gte, lte, lt, eq, gt, lte, like, in, numeric_between, date_between"
                err_mess="Operation not available : %s Allowed operations are : %s" % (operation,allowed_operations)           
                #self.__logger.error(err_mess)			
                raise Sitools2Exception(err_mess)  
        return kwargs 
    
    def __columnToDisplay(self, kwargs):
	output_name_list=[]
	output_name_dict={}                
        for outputCol in self.getOutputColumns():
            output_name_list.append(outputCol.getColumnAlias())
            output_name_dict.update({
                    outputCol.getColumnAlias() : outputCol
            })
	kwargs.update({#build colModel url options
		'colModel' : '"'+", ".join(output_name_list)+'"'
	})
        return kwargs
    
    def __buildSort(self):
        sort_dic_list=[]
        for column in self.getSorts():
            sort_dictionary={"field" : column.getColumnAlias(), "direction" : "ASC"}
            sort_dic_list.append(sort_dictionary)
	sort_kwargs={'sort' : {"ordersList" : sort_dic_list}}
        return urllib.urlencode(sort_kwargs).replace('+','').replace('%27','%22')        

    def __buildLimit(self, kwargs, limitResMax, nbResults):
        if limitResMax>0 and limitResMax < kwargs['limit']:
            kwargs['limit']=limitResMax
            kwargs['nocount']='true'
            nbResults = limitResMax
        elif  limitResMax>0 and  limitResMax >= kwargs['limit']:
            kwargs['nocount']='true'
            nbResults = limitResMax
        return [kwargs,nbResults]
        
    def __parseResponse(self, result):
        response = []
        for data in result['data'] :
            result_dict={}
            for k,v in data.items() :
                column = self.getOutputColumn(k)
                if column != None:
                    type = column.getSqlColumnType()
                    if type != None and type.startswith('int'): 
                        result_dict.update({
                                k : int(v)
                        })
                    elif type != None and type.startswith('float'):
                        result_dict.update({
                                k : float(v)
                        })
                    elif type != None  and type.startswith('timestamp'):
                        (dt, mSecs)= v.split(".")
                        dt = datetime.strptime(dt,"%Y-%m-%dT%H:%M:%S")
                        mSeconds = timedelta(microseconds = int(mSecs))
                        result_dict.update({
                                k : dt+mSeconds
                        })
                    else :
                        result_dict.update({
                                k : v
                        })                    
            response.append(result_dict)
        return response
                    
        
    def execute(self, limitRequest=350000, limitResMax=-1, **kwargs):
	kwargs.update({'media' : 'json','limit' : 300,'start' : 0})        
        kwargs = self.__buildFilter(kwargs)
        kwargs = self.__columnToDisplay(kwargs)
        sort_kwargs = self.__buildSort()
        url_count=self.__url+"/count"+'?'+urllib.urlencode(kwargs)+"&"+sort_kwargs
        url=self.__url+"/records"+'?'+urllib.urlencode(kwargs)+"&"+sort_kwargs
        result_count = _Util.retrieveJsonResponseFromServer(url_count)        
        nbr_results=result_count['total']
        resultSearch = []
        if nbr_results < limitRequest :
            [kwargs,nbr_results]  = self.__buildLimit(kwargs, limitResMax, nbr_results)
            url=self.__url+"/records"+'?'+urllib.urlencode(kwargs)+"&"+sort_kwargs            
            while (nbr_results-kwargs['start'])>0 :#Do the job per 300 items till nbr_result is reached
                resultTemp = _Util.retrieveJsonResponseFromServer(url)
                resultSearch.extend(self.__parseResponse(resultTemp))
                kwargs['start'] += kwargs['limit']#increment the job by the kwargs limit given (by design)  
		url=self.__url+"/records"+'?'+urllib.urlencode(kwargs)+"&"+sort_kwargs#encode new kwargs and build new url for request
        else:
            out_mess="Not allowed\nNbr results (%d) exceeds limit_request param: %d\n" % (nbr_results, limitRequest)
            self.__logger.info(out_mess)        
        return resultSearch
    
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()
#    try:
#        projects = Projects('http://medoc-dem.ias.u-psud.fr')
#        ps = projects.getProjects()
#        ps[0].display()
#    except Sitools2Exception as ex:
#        print ex.message


#>>> from pySitools2V2 import *
#>>> projects = Projects('http://medoc-dem.ias.u-psud.fr')
#URL to parse: http://medoc-dem.ias.u-psud.fr/ws_DEM_projet
#>>> ps = projects.getProjects()
#>>> p = ps[0]
#>>> dss = p.getDataSets()
#URL to parse: http://medoc-dem.ias.u-psud.fr/ws_SDO_DEM
#URL to parse: http://medoc-dem.ias.u-psud.fr/ws_DEM_HV
#>>> ds = dss.getDatasets()[0]
#>>> search = ds.getSearch()
#>>> c = search.getAvailableFilterCols()[1]
#>>> query = Query([c],['2'],'GTE')
#>>> search.addQuery(query)
#>>> search.execute()
    
