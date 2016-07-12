from sleekxmpp.xmlstream import ElementBase
from . import ShareItemStanza, AddressStanza


class ResourceStanza(ElementBase):
    """
    substanza for UserSharesStanza, one object represents one share
    """
    name = 'resource'
    namespace = 'https://xmpp.kwoh.de/protocol/shares'
    plugin_attrib = 'resource'
    interfaces = set(['resource'])
    plugin_multi_attrib = 'resources'  # does not show up in the real stanza, just for iterating from sleek

    def add_address(self, ip, port):
        # Use Param(None, self) to link the param object
        # with the task object.
        address = AddressStanza(None, self)  # links the item to self
        address['address'] = ip
        address['port'] = port

    def add_share(self, hash, name='', size=0):
        # Use Param(None, self) to link the param object
        # with the task object.
        share_obj = ShareItemStanza(None, self)  # links the item to self
        share_obj['hash'] = hash
        share_obj['name'] = name
        share_obj['size'] = str(size)
