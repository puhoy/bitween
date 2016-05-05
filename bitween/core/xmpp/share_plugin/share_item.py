from sleekxmpp.xmlstream import ElementBase

class ShareItem(ElementBase):
    """
    substanza for UserSharesStanza, one object represents one share
    """
    name = 'share'
    namespace = 'https://xmpp.kwoh.de/protocol/shares'
    plugin_attrib = 'share'
    interfaces = set(('name', 'hash', 'size'))
    plugin_multi_attrib = 'shares'