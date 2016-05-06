from sleekxmpp.xmlstream import ElementBase
from . import ShareItem

class UserSharesStanza(ElementBase):
    name = 'shares'
    namespace = 'https://xmpp.kwoh.de/protocol/shares'
    plugin_attrib = 'shares'
    interfaces = set(['ip', 'resource'])
    #sub_interfaces = interfaces

    def add_share(self, hash, name='', size=0):
        # Use Param(None, self) to link the param object
        # with the task object.
        share_obj = ShareItem(None, self)  # links the item to self
        share_obj['hash'] = hash
        share_obj['name'] = name
        share_obj['size'] = str(size)




