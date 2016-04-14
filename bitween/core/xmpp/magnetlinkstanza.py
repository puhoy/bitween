from xml.etree import cElementTree as et


class MagnetLinksStanza(object):
    def __init__(self, handles):
        root = et.Element("hashes")
        for h in handles:
            hash = et.Element("hash")
            hash.text = h.get('hash', '')

            size = et.Element("size")
            size.text = h.get('size', 0)

            name = et.Element("name")
            name.text = h.get("Name", "")

            hash.append(size)
            hash.append(name)
            root.append(hash)

        self.xml = root
        self.namespace = 'https://xmpp.kwoh.de/protocol/magnet_links'