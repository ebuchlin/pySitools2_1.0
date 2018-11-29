import unittest

from sitools2.clients import sdo_client_medoc


class MyTestCase(unittest.TestCase):
    def test_media_get(self):
        try:
            # self.assertRaises(ValueError("Nothing to download"), sdo_client_medoc.media_get())

            sdo_client_medoc.media_get()
            self.fail("No exception raised")
        except ValueError:
            pass
        except AssertionError:
            self.fail("exception")


if __name__ == '__main__':
    unittest.main()
