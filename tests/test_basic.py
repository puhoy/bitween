# -*- coding: utf-8 -*-

import unittest
import importlib
import imp

class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_lt_is_available(self):
        """ test libtorrent is available
        see http://stackoverflow.com/questions/14050281/how-to-check-if-a-python-module-exists-without-importing-it
        """
        try:
            imp.find_module('libtorrent')
            found = True
        except ImportError:
            found = False
        assert found

