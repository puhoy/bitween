from sleekxmpp.xmlstream import ElementBase
from . import ShareItemStanza


class ResourceStanza(ElementBase):
    """
    substanza for UserSharesStanza, one object represents one share
    """
    name = 'address'
    namespace = 'https://xmpp.kwoh.de/protocol/shares'
    plugin_attrib = 'address'
    interfaces = set(['resource', 'address', 'port'])
    plugin_multi_attrib = 'addresses'  # does not show up in the real stanza, just for iterating from sleek

    def add_share(self, hash, name='', size=0):
        # Use Param(None, self) to link the param object
        # with the task object.
        share_obj = ShareItemStanza(None, self)  # links the item to self
        share_obj['hash'] = hash
        share_obj['name'] = name
        share_obj['size'] = str(size)
