# -*- coding: utf-8 -*-

import unittest
import importlib
import imp

from bitween import components

class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_init(self):
        b = components.BitTorrentClient()
        assert b.name == 'bt'

    def test_exit(self):
        b = components.BitTorrentClient()
        components.publish('exit')
        b.handle_queue()

        assert b.end == True

if __name__ == '__main__':
    unittest.main()