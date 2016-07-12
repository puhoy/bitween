from sleekxmpp.xmlstream import ElementBase
from . import ResourceStanza


class UserSharesStanza(ElementBase):
    name = 'user_shares'
    namespace = 'https://xmpp.kwoh.de/protocol/shares'
    plugin_attrib = 'user_shares'

    def add_resource(self, resource=''):
        """

        :param ip:
        :param v: 'v4' or 'v6'
        :param port: the port bt is listening on
        :return:
        """
        resource_stanza = ResourceStanza(None, self)
        resource_stanza['resource'] = resource
        return resource_stanza


