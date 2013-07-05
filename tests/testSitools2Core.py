#! /usr/bin/python

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
#    along with this program.  If not, see <http://www.gnu.org/licenses

__author__="Jean-Christophe Malapert"
__date__ ="$9 juin 2013 11:38:58$"

import unittest
from sitools2.core.pySitools2 import *

class TestSitools2Core(unittest.TestCase):        
    
    def setUp(self):
        pass
    
    def testNbProjects(self):
        sitools2 = SITools2Instance('http://medoc-sdo.ias.u-psud.fr')
        projects = sitools2.getProjects()
        self.assertEqual( len(projects), 2)           
    
    def testDataIndex(self):
        dataset = DataSet( 'http://medoc-dem.ias.u-psud.fr', datasetName='ws_SDO_DEM')
        column = dataset.getColumns()[1]        
        self.assertEqual(column.getDataIndex(), "date_obs")
        
    def testGetHeader(self):
        dataset = DataSet( 'http://medoc-dem.ias.u-psud.fr', datasetName='ws_SDO_DEM')
        column = dataset.getColumns()[1]        
        self.assertEqual(column.getHeader(), "date_obs")

    def testIsSortable(self):
        dataset = DataSet( 'http://medoc-dem.ias.u-psud.fr', datasetName='ws_SDO_DEM')
        column = dataset.getColumns()[1]        
        self.assertEqual(column.isSortable(), True)
        
    def testIsVisible(self):
        dataset = DataSet( 'http://medoc-dem.ias.u-psud.fr', datasetName='ws_SDO_DEM')
        column = dataset.getColumns()[1]        
        self.assertEqual(column.isVisible(), True)
    
    def testIsFilter(self):
        dataset = DataSet( 'http://medoc-dem.ias.u-psud.fr', datasetName='ws_SDO_DEM')
        column = dataset.getColumns()[1]        
        self.assertEqual(column.isFilter(), True)
        
    def testIsPrimaryKey(self):
        dataset = DataSet( 'http://medoc-dem.ias.u-psud.fr', datasetName='ws_SDO_DEM')
        column = dataset.getColumns()[1]        
        self.assertEqual(column.isPrimaryKey(), False)
    
    def testHasRenderer(self):
        dataset = DataSet( 'http://medoc-dem.ias.u-psud.fr', datasetName='ws_SDO_DEM')
        column = dataset.getColumns()[1]        
        self.assertEqual(column.hasColumnRenderer(), False)
        
    def testGetColumnAlias(self):
        dataset = DataSet( 'http://medoc-dem.ias.u-psud.fr', datasetName='ws_SDO_DEM')
        column = dataset.getColumns()[1]        
        self.assertEqual(column.getColumnAlias(), "date_obs")
        
    def testSqlColumnType(self):
        dataset = DataSet( 'http://medoc-dem.ias.u-psud.fr', datasetName='ws_SDO_DEM')
        column = dataset.getColumns()[1]        
        self.assertEqual(column.getSqlColumnType(), "timestamp")
    
    def testOrderBy(self):
        dataset = DataSet( 'http://medoc-dem.ias.u-psud.fr', datasetName='ws_SDO_DEM')
        column = dataset.getColumns()[1]        
        self.assertEqual(column.getOrderBy(), "ASC")
        
    def testFormat(self):
        dataset = DataSet( 'http://medoc-dem.ias.u-psud.fr', datasetName='ws_SDO_DEM')
        column = dataset.getColumns()[1]        
        self.assertEqual(column.getFormat(), "Y-m-d H:i")

if __name__ == '__main__':
    unittest.main()
