from xml.etree import cElementTree as et


class MagnetLinksStanza(object):
    def __init__(self, magnetlinks):
        root = et.Element("magnet_links")
        for l in magnetlinks:
            link = et.Element("link")
            link.text = l
            root.append(link)
        self.xml = root
        self.namespace = 'https://xmpp.kwoh.de/protocol/magnet_links'