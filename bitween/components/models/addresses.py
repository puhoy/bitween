from . import logger
from .config import conf
from .helpers import get_ip_addresses
from .. import publish


class Addresses:
    def __init__(self, ports=None, ip_v4=None, ip_v6=None):
        """
        Model for storing own Addresses and Ports

        :param ports:
        :type ports: [int]
        :param ip_v4:
        :type ip_v4: [str]
        :param ip_v6:
        :type ip_v6: [str]
        """

        self.ip_v4 = []
        self.ip_v6 = []

        self.ports = []
        self.nat_ports = []

    def has_ip_v4(self):
        return self.ip_v4 is not []

    def has_ip_v6(self):
        return self.ip_v6 is not []

    def fetch_addresses(self):
        addresses = get_ip_addresses()

        if conf.get("enable_ipv4", False):
            self.ip_v4 = addresses.get('ip_v4', [])

        if conf.get("enable_ipv6", False):
            self.ip_v6 = addresses.get('ip_v6', [])
