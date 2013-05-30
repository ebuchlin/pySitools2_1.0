#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="malapert"
__date__ ="$29 mai 2013 23:01:03$"

from abc import ABCMeta, abstractmethod
from utility import Util, Sitools2Exception
#TODO use a decorator
class Query:
    __metaclass__ = ABCMeta
    
    p = -1
    f = -1

    @abstractmethod
    def getSyntax(self): pass       
        
class NumericBetween(Query):
    
    __PATTERN = "p[%s]=NUMERIC_BETWEEN|%s|%s|%s"
    
    def __init__(self, column, minVal, maxVal):
        self.__column = column
        self.__minVal = minVal
        self.__maxVal = maxVal    
        self.__validInputs()        
        
    def __validInputs(self):
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
        
    
    def getSyntax(self):
        Query.p+=1
        return self.__PATTERN % (str(Query.p), self.__column.getColumnAlias(), self.__minVal, self.__maxVal)
    

class DateBetween(Query):    
    
    def __init__(self, column, minDate, maxDate):
        self.__column = column
        self.__minDate = minDate
        self.__maxDate = maxDate
        #self.__validInputs()
        
    #def __validInputs(self):
    #    if not isinstance(self.__column, Column):
    #        raise Sitools2Exception("column must be an instance of Column")       
    
    def getSyntax(self):
        Query.p+=1
        parameter = {
        'p['+str(Query.p)+']' : 'DATE_BETWEEN|'+self.__column.getColumnAlias()+'|'+self.__minDate+'|'+self.__maxDate}
        return parameter
        

class EnumerateValues(Query):
    
    def __init__(self, column, enumerateValues):
        self.__column = column
        self.__enumerateVals = enumerateValues
        self.__validInputs()
        
    def __validInputs(self):
        #if not isinstance(self.__column, Column):
        #    raise Sitools2Exception("column must be an instance of Column")         
        if not isinstance(self.__enumerateVals, list):
            raise Sitools2Exception("enumerateValues must be a list")
    
    def getSyntax(self):
        Query.p+=1
        parameter = {
        'p['+str(Query.p)+']' : 'LISTBOXMULTIPLE|'+self.__column.getColumnAlias()+'|'+'|'.join(self.__enumerateVals)}
        return parameter
    

class StringEqual(Query):        
    
    def __init__(self, column, value):
        self.__column = column
        self.__value = value
        #self.__validInputs()
        
    #def __validInputs(self):
    #    if not isinstance(self.__column, Column):
    #        raise Sitools2Exception("column must be an instance of Column")         
        
    def getSyntax(self):
        Query.p+=1
        parameter = {
        'p['+str(Query.p)+']' : 'TEXTFIELD|'+self.__column.getColumnAlias()+'|'+self.__value}
        return parameter

class Filter(Query):

    __TYPE = ['numeric', 'string', 'boolean']
    __COMPARISON = ['LT', 'GT', 'EQ', 'LIKE' ,'IN', 'NOTIN']
    
    def __init__(self, column, type, value, comparison):
        self.__column = column
        self.__type = type
        self.__value = value
        self.__comparison = comparison
        self.__validInputs()
        
    def __validInputs(self):
        #if not isinstance(self.__column, Column):
        #    raise Sitools2Exception("column must be an instance of Column") 
        if self.__type not in self.__TYPE:
            raise Sitools2Exception("Type must be one of these values : numeric, string, boolean")
        if self.__comparison not in self.__COMPARISON:
            raise Sitools2Exception("Comparison must be one of these values : LT, GT, EQ, LIKE, IN, NOTIN")                
        
    def getSyntax(self):
        Query.f+=1
        parameter = {
        'filter['+str(Query.f)+'][columnAlias]' : self.__column.getColumnAlias(),
        'filter['+str(Query.f)+'][data][type]' : self.__type,
        'filter['+str(Query.f)+'][data][value]' : self.__value,
        'filter['+str(Query.f)+'][data][comparison]' : self.__comparison}
        return parameter

if __name__ == "__main__":
    query = NumericBetween("a",24, 35)
    syntax = query.getSyntax()
    print (syntax)
    query = NumericBetween("a",24, 35)
    syntax = query.getSyntax()
    print (syntax)
