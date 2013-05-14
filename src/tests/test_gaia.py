# To change this template, choose Tools | Templates
# and open the template in the editor.

import unittest
from sitools2.clients.gaia_client_idoc import *

class  Test_gaiaTestCase(unittest.TestCase):
    #def setUp(self):
    #    self.foo = Test_gaia()
    #

    #def tearDown(self):
    #    self.foo.dispose()
    #    self.foo = None

    def test_test_gaia(self):
        d1 = datetime(2012,8,10,0,0,0)
        d2 = d1 + timedelta(days=1)
        gaia_data_list = search( DATES=[d1,d2], nb_res_max=1 )
        get(GAIA_LIST=gaia_data_list, TARGET_DIR="/tmp")
        #assert x != y;
        #self.assertEqual(x, y, "Msg");
        
        self.fail("TODO: Write test")

if __name__ == '__main__':
    unittest.main()

