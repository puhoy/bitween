from threading import Lock

from . import logger

from .helpers import is_valid_ipv6_address
from .helpers import is_valid_ipv4_address


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
        get user dict

        :param jid:
        :return: dictionary with all data for user with jid
        """
        jid = str(jid)
        if not self.dict.get(jid, {}):
            self.dict[jid] = {}
        user = self.dict.get(jid, {})
        return user

    def get_resource(self, jid, resource):
        """
        get resource dict of user with JID jid

        :param jid:
        :param resource:
        :return:
        """
        jid = str(jid)
        user = self.get_user(jid)
        if not user.get(resource, False):
            user[resource] = {'ip_v4': [],
                              'ip_v6': [],
                              'shares': {}
                              }
        return user.get(resource)

    def add_address(self, jid, resource, address, port):
        """
        add Address and Port to Resource resource of jid

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

    def get_ipv4_addresses(self, jid, resource):
        """
        return all IPv4 Addresses of JIDs Resource resource

        :param jid:
        :param resource:
        :return: list of IPv4 Addresses
        """
        res = self.get_resource(jid, resource)
        return res.get('ip_v4', [])

    def get_ipv6_addresses(self, jid, resource):
        """
        return all IPv6 Addresses of JIDs Resource resource

        :param jid:
        :param resource:
        :return:
        """
        res = self.get_resource(jid, resource)
        return res.get('ip_v6', [])

    def clear_addresses(self, jid, resource):
        """
        clear Addresses of JIDs Resource

        :param jid:
        :param resource:
        :return:
        """
        res = self.get_resource(jid, resource)
        res['ip_v4'] = []
        res['ip_v6'] = []

    def clear_shares(self, jid, resource):
        """
        clear Shares of JIDs Resource

        :param jid:
        :param resource:
        :return:
        """
        res = self.get_resource(jid, resource)
        res['shares'] = {}

    def clear(self, jid, resource=None):
        """
        clear whole User with JID jid.
        If resource != None, clear resource of the JID

        :param jid:
        :param resource:
        :return:
        """
        jid = str(jid)
        if resource == None:
            self.dict[jid] = {}
        else:
            self.clear_addresses(jid, resource)
            self.clear_shares(jid, resource)


    def add_share(self, jid, resource, hash, name='', size=0, files=None):
        """
        Add a Share to a JIDs Resource

        :param jid:
        :param resource:
        :param hash: SHA1 Hash
        :type hash: str
        :param name: name of the share
        :type name: str
        :param size: size of the share in bytes
        :type size: int
        :param files: list of files in the Share
        :type files: list of str
        :return:
        """
        res = self.get_resource(jid, resource)
        res['shares'][hash] = {}
        res['shares'][hash]['name'] = name
        res['shares'][hash]['size'] = size
        res['shares'][hash]['files'] = files
        res['shares'][hash]['hash'] = hash

    def add_share_by_info(self, jid, resource, info):
        """
        add a share by torrent info

        :param jid:
        :param resource:
        :param info: dict from torrent_handles.get_shares()
        :return:
        """
        self.add_share(jid, resource, info.get('hash'), info.get('name', ''), info.get('total_size', 0))

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
