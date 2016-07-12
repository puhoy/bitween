from sleekxmpp.xmlstream import ElementBase
from . import ResourceStanza


class UserSharesStanza(ElementBase):
    name = 'shares'
    namespace = 'https://xmpp.kwoh.de/protocol/shares'
    plugin_attrib = 'shares'

    def add_resource(self, resource='', ip='', port=None):
        """

        :param ip:
        :param v: 'v4' or 'v6'
        :param port: the port bt is listening on
        :return:
        """
        addr_obj = ResourceStanza(None, self)
        addr_obj['resource'] = resource
        addr_obj['address'] = ip
        addr_obj['port'] = str(port)

        return addr_obj


