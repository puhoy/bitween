import logging

from sleekxmpp.plugins.base import BasePlugin
from . import stanza
from .stanza import UserSharesStanza, ShareItemStanza, AddressStanza

log = logging.getLogger(__name__)
from sleekxmpp.xmlstream import register_stanza_plugin

logger = logging.getLogger(__name__)


class UserShares(BasePlugin):
    """
    XEP-0118: User Tune
    """

    name = 'shares'
    description = 'UserShares'
    dependencies = set(['xep_0163'])
    stanza = stanza

    def plugin_end(self):
        self.xmpp['xep_0030'].del_feature(feature=UserShares.namespace)
        self.xmpp['xep_0163'].remove_interest(UserShares.namespace)
        pass

    def session_bind(self, jid):
        register_stanza_plugin(UserSharesStanza, ShareItemStanza, iterable=True)
        register_stanza_plugin(UserSharesStanza, AddressStanza, iterable=True)
        self.xmpp['xep_0163'].register_pep('shares', UserSharesStanza)

    def publish_shares(self, handles=None, addresses=None, options=None,
                       ifrom=None, block=True, callback=None, timeout=None):

        shares = UserSharesStanza()
        shares['resource'] = self.xmpp.boundjid.resource

        if handles:
            for h in handles:
                if h.get('hash', False):
                    shares.add_share(hash=h.get('hash'), name=h.get("name", None), size=h.get('total_size', None))
                else:
                    logger.error('NO HASH FOR HANDLE!')

        if addresses:
            for addr in addresses.ip_v4 + addresses.ip_v6:
                for port in addresses.ports + addresses.nat_ports:
                    logger.debug('adding address: %s:%s' % (addr, port))
                    shares.add_address(addr, port=port)


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

        self.publish_shares([])
