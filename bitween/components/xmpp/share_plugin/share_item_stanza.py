from sleekxmpp.xmlstream import ElementBase


class ShareItemStanza(ElementBase):
    """
    substanza for UserSharesStanza, one object represents one share
    """
    name = 'share_item'
    namespace = 'https://xmpp.kwoh.de/protocol/shares'
    plugin_attrib = 'share_item'
    interfaces = set(['name', 'hash', 'size'])
    plugin_multi_attrib = 'share_items'
