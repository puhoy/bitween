import netifaces
import ipgetter

import logging

logger = logging.getLogger(__name__)


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
        self.ip_v4 = addresses['ip_v4']
        self.ip_v6 = addresses['ip_v6']
        self.port = 0

    def has_ip_v4(self):
        return self.ip_v4 is not []

    def has_ip_v6(self):
        return self.ip_v6 is not []


def get_ip_addresses():
    # v4

    ## ask xmpp
    ## ipgetter

    ip_v4 = ""
    while not ip_v4:
        ip_v4 = ipgetter.myip()
        logger.debug('ipgetter got %s' % ip_v4)

    ## try upnp tricks
    ## parallel: wait for ip from bt

    # v6
    # get from system
    ip_v6 = []
    for interface in netifaces.interfaces():
        addresses = netifaces.ifaddresses(interface)[netifaces.AF_INET6]
        for address in addresses:
            if is_global(address['addr']):
                ip_v6.append(address['addr'])
    return {'ip_v4': [ip_v4],
            'ip_v6': ip_v6}


def is_global(address):
    # todo
    if address.startswith('fe80:') or address == '::1':
        return False
    else:
        return True
