import unittest

from sitools2.clients.idoc_medoc_client import idoc_medoc_search, idoc_medoc_get, idoc_medoc_get_selection,\
    idoc_medoc_metadata_search, metadata_info


class MyTestCase(unittest.TestCase):
    def test_idoc_medoc_search(self):
        try:
            # self.assertRaises(ValueError("Nothing to download"), sdo_client_medoc.media_get())
            idoc_medoc_search()
            self.fail("No exception raised")
        except ValueError:
            pass
        except AssertionError:
            self.fail("exception")

    def test_idoc_medoc_get(self):
        try:
            # self.assertRaises(ValueError("Nothing to download"), sdo_client_medoc.media_get())

            idoc_medoc_get()
            self.fail("No exception raised")
        except ValueError:
            pass
        except AssertionError:
            self.fail("exception")

    def test_idoc_medoc_get_selection(self):
        try:
            idoc_medoc_get_selection()
        except IOError:
            pass
        except ValueError:
            pass
        except AssertionError:
            self.fail("AssertionError")

    def test_metadata_search(self):
        try:
            idoc_medoc_metadata_search()

        except ValueError:
            pass
        except AssertionError:
            self.fail("Exception")

    def test_metada_info(self):
        try:
            metadata_info()
        except AssertionError:
            self.fail("Exception")
        except AttributeError:
            pass


if __name__ == '__main__':
    unittest.main()
