from sleekxmpp.plugins.base import BasePlugin
from . import stanza
from . import UserSharesStanza, ShareItemStanza, ResourceStanza
from sleekxmpp.xmlstream import register_stanza_plugin
import logging

from .. import Addresses

logger = logging.getLogger(__name__)


class UserShares(BasePlugin):
    """
    Share Plugin
    """

    name = 'shares'
    description = 'UserShares'
    dependencies = set(['xep_0163'])
    stanza = stanza

    def plugin_end(self):
        """


        :return:
        """
        self.xmpp['xep_0030'].del_feature(feature=UserShares.namespace)
        self.xmpp['xep_0163'].remove_interest(UserShares.namespace)
        pass

    def session_bind(self, jid):
        register_stanza_plugin(UserSharesStanza, ResourceStanza, iterable=True)
        register_stanza_plugin(UserSharesStanza, ShareItemStanza, iterable=True)
        self.xmpp['xep_0163'].register_pep('shares', UserSharesStanza)

    def publish_shares(self, handles=None, addresses=None, options=None,
                       ifrom=None, block=True, callback=None, timeout=None):
        """
        publish current shares and addresses

        :param handles:
        :param addresses:
        :param options:
        :param ifrom:
        :param block:
        :param callback:
        :param timeout:
        :return:
        """

        shares = UserSharesStanza()

        logging.info('publishing %s handles' % len(handles))

        logger.error(addresses.ip_v4 + addresses.ip_v6)
        logger.error(addresses.ports + addresses.nat_ports)

        self.resource_stanzas = []

        for addr in addresses.ip_v4 + addresses.ip_v6:
            for port in addresses.ports + addresses.nat_ports:
                logger.error('adding address: %s:%s' % (addr, port))
                self.resource_stanzas.append(shares.add_resource(self.xmpp.boundjid.resource, addr, port=port))

        if handles:
            for h in handles:
                if h.get('hash', False):
                    for stanza in self.resource_stanzas:
                        logging.info('adding hash %s of file %s' % (h.get('hash'), h.get("name", None)))
                        stanza.add_share(hash=h.get('hash'), name=h.get("name", None), size=h.get('total_size', None))
                else:
                    logger.error('NO HASH FOR HANDLE!')

        return self.xmpp['xep_0163'].publish(shares,
                                             node=UserSharesStanza.namespace,
                                             ifrom=ifrom,
                                             block=block,
                                             callback=callback,
                                             timeout=timeout)

    def stop(self, ifrom=None, block=True, callback=None, timeout=None):
        """
        Clear existing user tune information to stop notifications.
        """
        addresses = Addresses()
        self.publish_shares(handles=[], addresses=addresses)
