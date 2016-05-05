import logging
from threading import Lock
from time import time

from .torrentlist import TorrentList

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
