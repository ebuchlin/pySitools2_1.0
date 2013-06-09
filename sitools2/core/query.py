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
Decorator pattern to build a query to SITools2.

@author: Jean-Christophe MALAPERT
"""
__author__=["Jean-Christophe MALAPERT", "Pablo ALINGERY"]
__date__ ="$16 mai 2013 03:46:43$"
__credit__=["Jean-Christophe MALAPERT","Pablo ALINGERY", "Elie SOUBRIE"]
__maintainer__="Pablo ALINGERY"
__email__="jean-christophe.malapert@cnes.fr, pablo.alingery.ias.u-psud.fr, pablo.alingery@exelisvis.com"

try:
    from datetime import *
except:
    messageError = "Import failed in module pySitools2_idoc :\n\tdatetime module is required\n"
    sys.stderr.write(messageError)
    raise ImportError(messageError)

from utility import Util, Sitools2Exception, Log

try:
    import os
except:
    messageError = "Import failed in module pySitools2_idoc :\n\tos module is required\n"
    sys.stderr.write(messageError)
    raise ImportError(messageError)

class Query(object):
    """Abstract component to build a query. Thanks to the decorator pattern, it
    is possible to decorate the query by a set of constraints.
    
    Here is an example of the use of the decorator pattern.
    
    We start to create a Relative request :    
    >>> query = RelativeRequest();
    
    Now we decorate the relative request by a date constraint:    
    >>> query = DateBetween(query, "colDate", "25/05/20013", "26/05/2013")
    
    We go on to add a new date constraint:    
    >>> query = DateBetween(query, "colDate", "25/06/20013", "26/06/2013")
    
    Then we add a enumerate value constraint.
    >>> query = EnumerateValues(query, "col", ["val1", "val"])

    Finally, we get URL:
    >>> query.getUrl()
    '?p%5B2%5D=LISTBOXMULTIPLE%7Ccol%7Cval1%7Cval&start=0&limit=300&p%5B1%5D=DATE_BETWEEN%7CcolDate%7C25%2F06%2F20013%7C26%2F06%2F2013&media=json&p%5B0%5D=DATE_BETWEEN%7CcolDate%7C25%2F05%2F20013%7C26%2F05%2F2013'
    
    """
    
    def __init__(self):
        """Constructor."""
        self.__parameters = {'media' : 'json','limit' : 300,'start' : 0}
        self.__updateParams = {}
        self.__index = -1
        self.__filterIndex = -1
        self._url = ""        
    
    def _getIndex(self):
        """Returns the index to set for each parameter."""
        return self.__index
    
    def _getFilterIndex(self):
        """Returns the index to set for each filter."""
        return self.__filterIndex
    
    def _getParameters(self):
        """Returns the URL parameters that have been computed."""
        return  self.__parameters        
    
    def setBaseUrl(self, url):
        """Sets the base URL."""
        self._url = url
        
    def getBaseUrl(self):
        """Returns the base URL."""
        return self._url
    
    def getUrl(self):
        """Returns the complete URL."""
        return self._url + '?' + Util.urlencode(self._getParameters())
    
    
class RelativeRequest(Query):
    """Concrete component."""
    def __init__(self):
        super(RelativeRequest, self).__init__()

        
class DecoratorQuery(Query):
    """Decorator."""
    def __init__(self, query):
        super(DecoratorQuery, self).__init__()
        self.query = query
        self.__parameters = query._getParameters()
        
    def _getParameters(self):
        return self.__parameters
        

class NumericBetween(DecoratorQuery):
    """Decorates the query by a search between two numbers."""
    __PATTERN_VALUE = "NUMERIC_BETWEEN|%s|%s|%s"
    __PATTERN_KEY = "p[%s]"
    def __init__(self, query, column, minVal, maxVal):
        super(NumericBetween, self).__init__(query)
        self.__column = column
        self.__minVal = minVal
        self.__maxVal = maxVal
        self.__validInputs()
        
    def __validInputs(self):
        """Validates the inputs of the constructor."""
        #if not isinstance(self.__column, Column):
        #    raise Sitools2Exception("column must be an instance of Column")
        try:
            float(self.__minVal)
        except ValueError as ex:
            raise Sitools2Exception(ex)
        try:
            float(self.__maxVal)
        except ValueError as ex:
            raise Sitools2Exception(ex)
        
        if float(self.__minVal) >= float(self.__maxVal):
            raise Sitools2Exception("maxVal must be superior to minVal")        
    
    def _getParameters(self):
        """Returns the result of this decorator."""
        param = self.query._getParameters()
        key = self.__PATTERN_KEY % (str(self._getIndex()))
        val = self.__PATTERN_VALUE % (self.__column, self.__minVal, self.__maxVal)
        #self.__column.getColumnAlias()
        param.update({key:val})
        return param
    
    def _getIndex(self):        
        index = self.query._getIndex()
        return index+1
         
class DateBetween(DecoratorQuery):
    """Decorates the query by a search between two date."""
    __PATTERN_VALUE = "DATE_BETWEEN|%s|%s|%s"
    __PATTERN_KEY = "p[%s]"

    def __init__(self, query, column, minDate, maxDate):
        """Constructor."""
        super(DateBetween, self).__init__(query)
        self.__column = column
        self.__minDate = minDate
        self.__maxDate = maxDate    

    def _getParameters(self):
        """Returns the result of this decorator."""
        param = self.query._getParameters()
        key = self.__PATTERN_KEY % (str(self._getIndex()))
        val = self.__PATTERN_VALUE % (self.__column, self.__minDate, self.__maxDate)
        #self.__column.getColumnAlias()
        param.update({key:val})        
        return param
    
    def _getIndex(self):
        index = self.query._getIndex()
        return index+1
    

class EnumerateValues(DecoratorQuery):
    """Decorates the query by a search based of a list of values."""
    __PATTERN_VALUE = "LISTBOXMULTIPLE|%s|%s"
    __PATTERN_KEY = "p[%s]"

    def __init__(self, query, column, enumerateValues):
        """Constructor."""
        super(EnumerateValues, self).__init__(query)
        self.__column = column
        self.__enumerateValues = enumerateValues
        self.__validInputs()
        
    def __validInputs(self):
        """Validates the inputs of the constructor."""
        #if not isinstance(self.__column, Column):
        #    raise Sitools2Exception("column must be an instance of Column")         
        if not isinstance(self.__enumerateValues, list):
            raise Sitools2Exception("enumerateValues must be a list")        

    def _getParameters(self):
        """Returns the result of this decorator."""
        param = self.query._getParameters()
        key = self.__PATTERN_KEY % (str(self._getIndex()))
        val = self.__PATTERN_VALUE % (self.__column, '|'.join(self.__enumerateValues))
        #self.__column.getColumnAlias()
        param.update({key:val})
        return param
    
    def _getIndex(self):
        index = self.query._getIndex()
        return index+1

class StringEqual(DecoratorQuery):
    """Decorates the query by a text search."""
    __PATTERN_VALUE = "TEXTFIELD|%s|%s"
    __PATTERN_KEY = "p[%s]"

    def __init__(self, query, column, value):
        """Constructor."""
        super(StringEqual, self).__init__(query)
        self.__column = column
        self.__value = value

    def _getParameters(self):
        """Returns the result of this decorator."""
        param = self.query._getParameters()
        key = self.__PATTERN_KEY % (str(self._getIndex()))
        val = self.__PATTERN_VALUE % (self.__column, self.__value)
        #self.__column.getColumnAlias()
        param.update({key:val})
        return param
    
    def _getIndex(self):
        index = self.query._getIndex()
        return index+1    
    
class Filter(DecoratorQuery):
    """Decorates the query by filters."""
    __TYPE = ['numeric', 'string', 'boolean']
    __COMPARISON = ['LT', 'GT', 'EQ', 'LIKE' ,'IN', 'NOTIN']
    
    def __init__(self, query, column, type, value, comparison):
        """Cosntrcutor."""
        super(Filter, self).__init__(query)
        self.__column = column
        self.__type = type
        self.__value = value
        self.__comparison = comparison
        self.__validInputs()
        
    def __validInputs(self):
        """Validates the inputs of the constructor."""
        #if not isinstance(self.__column, Column):
        #    raise Sitools2Exception("column must be an instance of Column") 
        if self.__type not in self.__TYPE:
            raise Sitools2Exception("Type must be one of these values : numeric, string, boolean")
        if self.__comparison not in self.__COMPARISON:
            raise Sitools2Exception("Comparison must be one of these values : LT, GT, EQ, LIKE, IN, NOTIN")                

    def _getParameters(self):
        """Returns the result of this decorator."""
        param = self.query._getParameters() 
        index = self._getFilterIndex()
        param.update({
        'filter['+str(index)+'][columnAlias]' : self.__column,
        'filter['+str(index)+'][data][type]' : self.__type,
        'filter['+str(index)+'][data][value]' : self.__value,
        'filter['+str(index)+'][data][comparison]' : self.__comparison})        
        #self.__column.getColumnAlias()
        return param
    
    def _getFilterIndex(self):
        index = self.query._getFilterIndex()
        return index+1
    
class ColumnToDisplay(DecoratorQuery):
    """Decorates the query by setting the columns to display."""
    def __init__(self, query, columns):
        """Constructor."""
        super(ColumnToDisplay, self).__init__(query)
        self.__columns = columns       
        
    def _getParameters(self):
        """Returns the result of this decorator."""
        param = self.query._getParameters() 
        outputNames = []
        for outputCol in self.__columns:
            outputNames.append(outputCol)            
        param.update({'colModel' : '"'+', '.join(outputNames)+'"'})        
        return param
    
class Sorting(DecoratorQuery):
    """Decorates the query by setting the columns to sort."""
    def __init__(self, query, columns):
        """Constructor."""
        super(Sorting, self).__init__(query)
        self.__columns = columns     
        
    def _getParameters(self):
        """Returns the result of this decorator."""
        param = self.query._getParameters()        
        sortingNames = []
        for outputCol in self.__columns:
            sort_dictionary={"field" : outputCol, "direction" : "ASC"}
            sortingNames.append(sort_dictionary)            
        param.update({'sort' : {"ordersList" : sortingNames}})
        return param


class UpdateParameter(DecoratorQuery):
    """Decorates the query by updating a parameter."""
    def __init__(self, query, key, value):
        """Constructor."""
        super(UpdateParameter, self).__init__(query)
        self.__key = key
        self.__value = value
        
    def _getParameters(self):
        """Returns the result of this decorator."""
        param = self.query._getParameters()                   
        param[self.__key] =  self.__value
        return param        

class Search:
    """The search capabilities."""
    LOGICAL_OPERATORS = ['LT', 'EQ', 'GT', 'LTE', 'GTE']
    
    def __init__(self, columns, url):
        self.__logger = Log.getLogger(self.__class__.__name__)
        self.__columns = []
        self.__availableFilterCols = []
        self.__availableSortableCols = []
        self.__queryParameters = None
        self.__outputColumns = columns
        self.__url = url
        for column in columns:
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
        """Returns the available columns that can be filtered."""
        return self.__availableFilterCols
    
    def getAvailableSortCols(self):
        """Returns the available columns that can be sorted."""
        return self.__availableSortableCols    
    
    def getColumns(self):
        """Returns the columns."""
        return self.__columns
        
    def setQueries(self, queryParameters):
        """Sets the Query."""
        if not isinstance(queryParameters, Query):
            raise Sitools2Exception("queryParameters must be an instance of Query")
        self.__queryParameters = queryParameters
    
    def getQueries(self):
        """Returns the Query."""
        return self.__queryParameters     
    
    def getOutputColumns(self):
        """Returns the columns to display."""
        return self.__outputColumns
    
    def getOutputColumn(self, columnAlias):
        """Returns a Column."""
        result = None
        for column in self.__outputColumns:
            if column.getColumnAlias() == columnAlias:
                result = column
                break
        return result         

    def __buildLimit(self, query ,limitResMax):
        """Builds limit parameter."""
        limit = query._getParameters()['limit']
        if limitResMax>0 and limitResMax < limit:
            query = UpdateParameter(query, 'limit', limitResMax)
            query = UpdateParameter(query, 'nocount', 'true')        
        elif  limitResMax>0 and  limitResMax >= limit:
            query = UpdateParameter(query, 'nocount', 'true')
        return query
        
    def __parseResponse(self, result):
        """Parses the server response."""
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
    
    def download(self, FILENAME=None):
        """Downloads the files related to the query."""
        resultFilename = None
        url = self.__url+'/services'                
        result = Util.retrieveJsonResponseFromServer(url)
        dataItems = result['data']
        for item in dataItems:
            plugin = Plugin(item)        
            result = plugin.getParameterByValue("fr.cnes.sitools.resources.order.DirectOrderResource")            
            if result == None:
                continue
            else:
                urlParameter = plugin.getParameterByType('PARAMETER_ATTACHMENT')
                urlPlugin = urlParameter.getValue()
                encodingParameter = plugin.getParameterByName('archiveType')
                encodingPlugin = encodingParameter.getValue()
                query = self.getQueries()
                query.setBaseUrl(self.__url + urlPlugin)
                url = query.getUrl()                
                (filename, header) = Util.urlretrieve('%s' % url, FILENAME)
                if FILENAME == None:
                    os.rename(filename, filename + "." + encodingPlugin)
                    resultFilename = filename + "." + encodingPlugin
                else:
                    os.rename(FILENAME, FILENAME + "." + encodingPlugin)
                    resultFilename = FILENAME + "." + encodingPlugin
                break
        return resultFilename
    
    def execute(self, limitRequest=350000, limitResMax=-1):
        """Executes the query."""
        query = self.getQueries()
        query  = self.__buildLimit(query, limitResMax)
        nbr_results = limitResMax
        if (limitResMax == -1):
            query.setBaseUrl(self.__url+'/count')
            countUrl = query.getUrl()            
            result_count = Util.retrieveJsonResponseFromServer(countUrl)    
            nbr_results=result_count['total']
        else:
            nbr_results = limitResMax
        resultSearch = []
        if nbr_results < limitRequest :            
            query.setBaseUrl(self.__url+'/records')
            url = query.getUrl()
            startVal = query._getParameters()['start']
            while (nbr_results-startVal)>0 :#Do the job per 300 items till nbr_result is reached                
                resultTemp = Util.retrieveJsonResponseFromServer(url)
                resultSearch.extend(self.__parseResponse(resultTemp))
                parameters = query._getParameters()                
                startVal = parameters['start'] + parameters['limit']
                query = UpdateParameter(query, 'start', startVal) 
                query.setBaseUrl(self.__url+'/records')
		url=query.getUrl()            
        else:
            out_mess="Not allowed\nNbr results (%d) exceeds limit_request param: %d\n" % (nbr_results, limitRequest)
            self.__logger.info(out_mess)        
        return resultSearch        
        
class Plugin:
    """SITools2 plugin on the dataset."""
    def __init__(self, data):
        """Constrcutor."""
        self.__data = data        
        self.__parseParameters()
        
    def __parseParameters(self):
        """Parses the parameters of data."""
        self.__parameters = []
        for parameter in self.__data['parameters']:
            self.__parameters.append(Parameter(parameter))

    def getName(self):
        """Returns the plugin name."""
        return self.__data['name']
    
    def getDescription(self):
        """Returns the plugin description."""
        if self.__data.has_key('description'):
            return self.__data['description']
        else:
            return None
    
    def getParameters(self):
        """Returns the plugin parameters."""
        return self.__parameters
    
    def getParameterByValue(self, value):
        """Searchs a parameter by value and returns it."""
        result = None
        for parameter in self.getParameters():
            valueParam = parameter.getValue()
            if valueParam == value:
                result = parameter
                break
        return result
    
    def getParameterByType(self, type):
        """Searchs a parameter by type and returns it."""
        result = None
        for parameter in self.getParameters():
            typeParam = parameter.getType()
            if typeParam == type:
                result = parameter
                break
        return result        
    
    def getParameterByName(self, name):
        """Searchs a parameter by name and returns it."""
        result = None
        for parameter in self.getParameters():
            nameParam = parameter.getName()
            if nameParam == name:
                result = parameter
                break
        return result      
    
    def getDataSetSelection(self):
        """Returns the dataset selection."""
        return self.__data['dataSetSelection']

    def getBehavior(self):
        """Returns the behavior."""
        if self.__data.has_key('behavior'):
            return self.__data['behavior']
        else:
            return None        
    
class Parameter:
    """Hanles plugin parameter."""
    def __init__(self, data):
        """Constructor."""
        self.__parameter = data
    
    def getName(self):
        """Returns the parameter name."""
        return self.__parameter['name']
    
    def getDescription(self):
        """Returns the description name."""
        return self.__parameter['description']
    
    def getValue(self):
        """Returns the value name."""
        return self.__parameter['value']
    
    def getValueType(self):
        """Returns the value type."""
        return self.__parameter['valueType']
    
    def getType(self):
        """Returns the type."""
        return self.__parameter['type']  
    
def test(): 
    import doctest
    doctest.testmod()
    
if __name__ == "__main__":
    test()
