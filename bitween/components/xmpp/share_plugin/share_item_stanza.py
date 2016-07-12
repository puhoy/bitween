from sleekxmpp.xmlstream import ElementBase


class ShareItemStanza(ElementBase):
    """
    substanza for UserSharesStanza, one object represents one share
    """
    name = 'share'
    namespace = 'https://xmpp.kwoh.de/protocol/shares'
    plugin_attrib = 'share'
    interfaces = set(['name', 'hash', 'size'])
    plugin_multi_attrib = 'share_items'
