from sleekxmpp.xmlstream import ElementBase, ET


class UserSharesStanza(ElementBase):
    name = 'shares'
    namespace = 'https://xmpp.kwoh.de/protocol/magnet_links'
    plugin_attrib = 'shares'
    interfaces = set(['ip', 'shares'])
    sub_interfaces = interfaces

