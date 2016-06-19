from sleekxmpp.xmlstream import ElementBase



class AddressStanza(ElementBase):
    """
    substanza for UserSharesStanza, one object represents one share
    """
    name = 'address'
    namespace = 'https://xmpp.kwoh.de/protocol/shares'
    plugin_attrib = 'address'
    interfaces = set(['address', 'port'])
    plugin_multi_attrib = 'addresses'  # does not show up in the real stanza, just for iterating from sleek
