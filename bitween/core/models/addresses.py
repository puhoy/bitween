import netifaces
import ipgetter

class Addresses:
    def __init__(self, ports=None, ip_v4=None, ip_v6=None):
        if ip_v6 is None:
            ip_v6 = []
        if ip_v4 is None:
            ip_v4 = []
        self.ip_v4 = ip_v4
        self.ip_v6 = ip_v6

        if ports is None:
            ports = []
        self.ports = ports

    def has_ip_v4(self):
        return self.ip_v4 is not []

    def has_ip_v6(self):
        return self.ip_v6 is not []


def get_ip_addresses():
    # v4
    ip_v4 = []
    ipgetter.myip()
    ## ask xmpp
    ## ipgetter
    ## try upnp tricks
    ## parallel: wait for ip from bt

    # v6
    # get from system
    ip_v6 = []
    for interface in netifaces.interfaces():
        address = netifaces.ifaddresses(interface)[netifaces.AF_INET6]
        if is_global(address):
            ip_v6.append(address)
    return {'ip_v4': ip_v4,
            'ip_v6': ip_v6}

def is_global(address):
    # todo
    return True
