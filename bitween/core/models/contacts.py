import logging
from threading import Lock
from time import time

logger = logging.getLogger(__name__)

import socket


# check methods from http://stackoverflow.com/questions/319279/how-to-validate-ip-address-in-python
def is_valid_ipv4_address(address):
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:  # no inet_pton here, sorry
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:  # not a valid address
        return False

    return True


def is_valid_ipv6_address(address):
    try:
        socket.inet_pton(socket.AF_INET6, address)
    except socket.error:  # not a valid address
        return False
    return True


class UserShares:
    def __init__(self):
        self.dict = {}
        """
        self.dict = {
            'user@server': {
                'resource': {
                    "ip_v4": [],
                    "ip_v6": [],
                    "port": 0
                    "shares": {
                        'some_hash': {
                            'hash': 'some_hash',
                            'name': '',
                            'size': 0,
                            'files': []
                        }
                    }
                }
            }
        }
        """
        self.lock = Lock()

    def get_user(self, jid):
        if not self.dict.get(jid, {}):
            self.dict[jid] = {}
        user = self.dict.get(jid, {})
        return user

    def get_resource(self, jid, resource):
        user = self.get_user(jid)
        if not user.get(resource, {}):
            user[resource] = {'ip_v4': '',
                              'ip_v6': '',
                              'shares': {}
                              }
        return user.get(resource)

    def set_port(self, jid, resource, port):
        res = self.get_resource(jid, resource)
        res['port'] = port

    def add_address(self, jid, resource, address):
        res = self.get_resource(jid, resource)
        if is_valid_ipv4_address(address):
            res['ip_v4'].append(address)
        elif is_valid_ipv6_address(address):
            res['ip_v6'].append(address)
        else:
            logger.error('invalid address: %s' % address)

    def clear_addresses(self, jid, resource):
        res = self.get_resource(jid, resource)
        res['ip_v4'] = []
        res['ip_v6'] = []
        res["port"] = 0

    def clear_shares(self, jid, resource):
        """

        :param jid:
        :param resource:
        :param shares: a dict list with dicts like {'hash': xxx, 'name': '', size: 0, files: ['one', 'two']}
        :return:
        """

        res = self.get_resource(jid, resource)
        res['shares'] = {}

    def add_share(self, jid, resource, hash, name='', size=0, files=None):
        res = self.get_resource(jid, resource)
        res['shares'][hash] = {}
        res['shares'][hash]['name'] = name
        res['shares'][hash]['size'] = size
        res['shares'][hash]['files'] = files
        res['shares'][hash]['hash'] = hash

    def __iter__(self):
        with self.lock:
            for x, y in self.dict:
                yield x, y

    def __getitem__(self, item):
        with self.lock:
            return self.dict[item]

    def __setitem__(self, key, value):
        with self.lock:
            self.dict[key] = value

    def __delitem__(self, key):
        with self.lock:
            del self.dict[key]

    @property
    def hashes(self):
        """
        returns a dict with all hashes and a list of ip_port tuples for each hash

        :return:
        """
        h = {}
        for user in self.dict.keys():
            logger.debug(user)
            for resource in self.dict[user].keys():
                logger.debug(resource)
                for share in self.dict[user][resource]['shares']:
                    logger.debug(share)
                    hash = self.dict[user][resource]['shares'][share]['hash']
                    if not h.get(hash, False):
                        h[hash] = []
                    for address in self.dict[user][resource]['ip_v4'] + self.dict[user][resource]['ip_v6']:
                        address_tuple = (address, self.dict[user][resource]['port'])

                        if address_tuple not in h[hash]:
                            h[hash].append(
                                (address, self.dict[user][resource]['port']))

        return h
