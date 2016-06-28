import netifaces
import ipgetter

from . import logger
from .. import conf
from ..helpers import get_ip_addresses


class Addresses:
    def __init__(self, ports=None, ip_v4=None, ip_v6=None):
        """

        :param ports:
        :param ip_v4:
        :param ip_v6:
        """
        """
        if ip_v6 is None:
            ip_v6 = []
        if ip_v4 is None:
            ip_v4 = []
        self.ip_v4 = ip_v4
        self.ip_v6 = ip_v6

        if ports is None:
            ports = []
        self.ports = ports
        """
        addresses = get_ip_addresses()

        if conf.get("enable_ipv4", False):
            self.ip_v4 = addresses.get('ip_v4', [])
        else:
            self.ip_v4 = []

        if conf.get("enable_ipv6", False):
            self.ip_v6 = addresses.get('ip_v6', [])
        else:
            self.ip_v6 = []

        self.ports = []
        self.nat_ports = []

    def has_ip_v4(self):
        return self.ip_v4 is not []

    def has_ip_v6(self):
        return self.ip_v6 is not []





