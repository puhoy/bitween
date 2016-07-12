from sleekxmpp.xmlstream import ElementBase
from . import ShareItemStanza, AddressStanza


class UserSharesStanza(ElementBase):
    name = 'shares'
    namespace = 'https://xmpp.kwoh.de/protocol/shares'
    plugin_attrib = 'shares'
    interfaces = set(['resource'])

    def add_share(self, hash, name='', size=0):
        # Use Param(None, self) to link the param object
        # with the task object.
        share_obj = ShareItemStanza(None, self)  # links the item to self
        share_obj['hash'] = hash
        share_obj['name'] = name
        share_obj['size'] = str(size)

    def add_address(self, ip='', port=None):
        """

        :param ip:
        :param v: 'v4' or 'v6'
        :param port: the port bt is listening on
        :return:
        """
        addr_obj = AddressStanza(None, self)
        addr_obj['address'] = ip
        addr_obj['port'] = str(port)




