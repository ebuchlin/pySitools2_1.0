#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="malapert"
__date__ ="$30 mai 2013 01:03:53$"

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
        return urllib.urlencode(param).replace('+','').replace('%27','%22')
    
    @staticmethod
    def urlretrieve(url, FILENAME = None):
        return urllib.urlretrieve('%s' % url, FILENAME)   

class Sitools2Exception(Exception):
    """SITools2 Exception"""
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)

if __name__ == "__main__":
    print "Hello World";
