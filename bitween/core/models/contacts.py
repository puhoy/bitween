import logging
from threading import Lock
from time import time

logger = logging.getLogger(__name__)


class UserShares:
    def __init__(self):
        self.dict = {}
        """
        self.dict = {
            'user@server': {
                'resource': {
                    "ip_v4": '',
                    "ip_v6": '',
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
        returns a dict with all hashes and a list of ips for each hash

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
                        h[hash] = {'ip_v4': [],
                                   'ip_v6': []}
                    if self.dict[user][resource]['ip_v4']:
                        if self.dict[user][resource]['ip_v4'] not in h[hash]['ip_v4']:
                            h[hash]['ip_v4'].append(self.dict[user][resource]['ip_v4'])
                    if self.dict[user][resource]['ip_v6']:
                        if self.dict[user][resource]['ip_v6'] not in h[hash]['ip_v6']:
                            h[hash]['ip_v6'].append(self.dict[user][resource]['ip_v6'])
        return h
