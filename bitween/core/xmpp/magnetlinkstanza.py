from xml.etree import cElementTree as et
import logging
logger = logging.getLogger(__name__)


class MagnetLinksStanza(object):
    def __init__(self, handles):
        root = et.Element("hashes")
        for h in handles:
            hash = et.Element("hash", size=str(h.get('total_size', 0)), name=h.get("name", ""))
            hash.text = h.get('hash', '')

            root.append(hash)

        self.xml = root
        self.namespace = 'https://xmpp.kwoh.de/protocol/magnet_links'