from sleekxmpp.xmlstream import ElementBase

class ShareItem(ElementBase):
    """
    substanza for UserSharesStanza, one object represents one share
    """
    name = 'address'
    namespace = 'https://xmpp.kwoh.de/protocol/shares#address'
    plugin_attrib = 'address'
    interfaces = set(['address', 'type'])
    plugin_multi_attrib = 'addresses'