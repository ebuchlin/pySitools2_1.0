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

__author__=["Jean-Christophe MALAPERT", "Pablo ALINGERY"]
__date__ ="$16 mai 2013 03:46:43$"
__credit__=["Jean-Christophe MALAPERT","Pablo ALINGERY", "Elie SOUBRIE"]
__maintainer__="Pablo ALINGERY"
__email__="jean-christophe.malapert@cnes.fr, pablo.alingery.ias.u-psud.fr, pablo.alingery@exelisvis.com"


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
    import logging
except:
    messageError = "Import failed in module pySitools2_idoc :\n\tlogging module is required\n"
    sys.stderr.write(messageError)
    raise ImportError(messageError)

class Util(object):
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
    
    @staticmethod
    def urlencode(param):
        """Returns the URL parameters encoded."""
        return urllib.urlencode(param).replace('+',' ').replace('%27','%22')
    
    @staticmethod
    def urlretrieve(url, FILENAME = None):
        """Retrieves a file from an URL."""
        return urllib.urlretrieve('%s' % url, FILENAME)   

class Sitools2Exception(Exception):
    """SITools2 Exception"""
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)


class Log(object):
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
    
if __name__ == "__main__":
    print "Hello World";
