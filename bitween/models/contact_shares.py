from threading import Lock

from . import logger
import socket


from helpers import is_valid_ipv6_address
from helpers import is_valid_ipv4_address


class ContactShares:
    """
    this class holds all the discovered UserShares
    """

    def __init__(self):
        """
        this class holds all the discovered UserShares

        basically it works as a wrapper around a dict with the following structure:

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
        self.dict = {}  # StoredDict('user_cache.json', autocommit=True)
        self.lock = Lock()

    def get_user(self, jid):
        """

        :param jid:
        :return:
        """
        if not self.dict.get(jid, {}):
            self.dict[jid] = {}
        user = self.dict.get(jid, {})
        return user

    def get_resource(self, jid, resource):
        """

        :param jid:
        :param resource:
        :return:
        """
        user = self.get_user(jid)
        if not user.get(resource, {}):
            user[resource] = {'ip_v4': '',
                              'ip_v6': '',
                              'shares': {}
                              }
        return user.get(resource)

    def add_address(self, jid, resource, address, port):
        """

        :param jid:
        :param resource:
        :param address:
        :param port:
        :return:
        """
        res = self.get_resource(jid, resource)
        if is_valid_ipv4_address(address):
            res['ip_v4'].append((address, port))
        elif is_valid_ipv6_address(address):
            res['ip_v6'].append((address, port))
        else:
            logger.error('invalid address: %s' % address)

    def clear_addresses(self, jid, resource):
        """

        :param jid:
        :param resource:
        :return:
        """
        res = self.get_resource(jid, resource)
        res['ip_v4'] = []
        res['ip_v6'] = []

    def clear_shares(self, jid, resource):
        """

        :param jid:
        :param resource:
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
                    for (address, port) in self.dict[user][resource]['ip_v4'] + self.dict[user][resource]['ip_v6']:
                        address_tuple = (address, port)
                        if address_tuple not in h[hash]:
                            h[hash].append(
                                (address, port))

        return h
