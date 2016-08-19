import netifaces
import ipgetter
import socket

import logging

logger = logging.getLogger(__name__)


def is_global(address):
    """
    check if address is a global IPv6 address

    :param address:
    :return:
    """
    # todo
    if address.startswith('fe80:') or address == '::1':
        return False
    else:
        return True


def get_ip_addresses():
    """
    try to get own ip addresses

    right now this would discover one IPv4 address (the one ipgetter is returning)
    and all global IPv6 addresses netifaces reads from the system


    :return: {'ip_v4': [ip_v4_addresses], # one IPv4 address in a list
            'ip_v6': ip_v6}  # a list of IPv6 addresses
    """
    # TODO:
    # in future we need more ways to discover our own addresses,
    # for example getting addresses via upnp or from other BitTorrent clients we may have discovered


    ip_v4 = ""
    while not ip_v4:
        logger.info('getting ip...')
        ip_v4 = ipgetter.myip()
        logger.debug('ipgetter got %s' % ip_v4)

    ip_v6 = []
    for interface in netifaces.interfaces():
        try:
            addresses = netifaces.ifaddresses(interface)[netifaces.AF_INET6]
            for address in addresses:
                if is_global(address['addr']):
                    ip_v6.append(address['addr'])
        except KeyError as e:
            logger.debug('Error while getting address from interface %s: %s' % (interface, e))

    return {'ip_v4': [ip_v4],
            'ip_v6': ip_v6}


# check methods from http://stackoverflow.com/questions/319279/how-to-validate-ip-address-in-python
def is_valid_ipv4_address(address):
    """
    from http://stackoverflow.com/questions/319279/how-to-validate-ip-address-in-python

    checks if an address is a valid ipv4 address

    :param address:
    :return:
    """
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
    """
    from http://stackoverflow.com/questions/319279/how-to-validate-ip-address-in-python

    checks if an address is a valid ipv6 address

    :param address:
    :return:
    """
    try:
        socket.inet_pton(socket.AF_INET6, address)
    except socket.error:  # not a valid address
        return False
    return True
