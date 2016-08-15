# -*- coding: utf-8 -*-

import unittest
import importlib
import imp

from bitween import components


class ModelsTestSuite(unittest.TestCase):
    def test_addresses(self):
        a = components.Addresses()
        a.fetch_addresses()
        assert a.has_ip_v4() is True

    def test_contact_shares(self):
        shares = components.contact_shares

        some_ipv6 = '2a02:2028:530:7901:d250:99ff:fe49:3cb0'
        some_ipv4 = '1.1.1.1'

        hash = '11111111111'
        size = 123
        files = ['filename']
        name = 'name'

        assert shares.dict == {}

        assert shares.get_user('new_user') == {}
        assert shares.get_resource('new_user',
                                   'new_resource') == {'ip_v4': [],
                                                       'ip_v6': [],
                                                       'shares': {}}

        shares.add_address('new_user', 'new_resource', some_ipv4, 11)
        shares.add_address('new_user', 'new_resource', some_ipv6, 11)
        assert shares.get_ipv4_addresses('new_user', 'new_resource') == [(some_ipv4, 11)]
        assert shares.get_ipv6_addresses('new_user', 'new_resource') == [(some_ipv6, 11)]

        shares.add_share('new_user', 'new_resource', hash, name, size, files)

        assert shares.hashes == {
            hash: shares.get_ipv4_addresses('new_user', 'new_resource') +
                  shares.get_ipv6_addresses('new_user', 'new_resource')
        }

if __name__ == '__main__':
    unittest.main()