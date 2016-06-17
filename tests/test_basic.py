# -*- coding: utf-8 -*-

import unittest
from app import some_app_file

class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_some_app_file(self):
        """ test app_function """
        ret_string = some_app_file.app_function()
        assert ret_string is 'regular'


if __name__ == '__main__':
    unittest.main()
