import logging

from sleekxmpp.plugins.base import BasePlugin
from . import stanza
from .stanza import UserSharesStanza
from xml.etree import cElementTree as et
from xml.etree.ElementTree import tostring
log = logging.getLogger(__name__)


class UserShares(BasePlugin):
    """
    XEP-0118: User Tune
    """

    name = 'shares'
    description = 'UserShares'
    dependencies = set(['xep_0163'])
    namespace = 'https://xmpp.kwoh.de/protocol/magnet_links'
    stanza = stanza

    def plugin_end(self):
        self.xmpp['xep_0030'].del_feature(feature=UserShares.namespace)
        self.xmpp['xep_0163'].remove_interest(UserShares.namespace)

    def session_bind(self, jid):
        self.xmpp['xep_0163'].register_pep('shares', UserSharesStanza)

    def publish_shares(self, handles, ip, options=None,
                       ifrom=None, block=True, callback=None, timeout=None):

        tune = UserSharesStanza()
        tune['ip'] = ip
        tune['shares'] = {}

        for h in handles:
            # todo
            tune['shares'] = tostring(et.Element("hash", size=str(h.get('total_size', 0)), name=h.get("name", "")))

        return self.xmpp['xep_0163'].publish(tune,
                                             node=UserShares.namespace,
                                             ifrom=ifrom,
                                             block=block,
                                             callback=callback,
                                             timeout=timeout)


def stop(self, ifrom=None, block=True, callback=None, timeout=None):
    """
    Clear existing user tune information to stop notifications.

    Arguments:
        ifrom    -- Specify the sender's JID.
        block    -- Specify if the send call will block until a response
                    is received, or a timeout occurs. Defaults to True.
        timeout  -- The length of time (in seconds) to wait for a response
                    before exiting the send call if blocking is used.
                    Defaults to sleekxmpp.xmlstream.RESPONSE_TIMEOUT
        callback -- Optional reference to a stream handler function. Will
                    be executed when a reply stanza is received.
    """
    tune = UserTune()
    return self.xmpp['xep_0163'].publish(tune,
                                         node=UserTune.namespace,
                                         ifrom=ifrom,
                                         block=block,
                                         callback=callback,
                                         timeout=timeout)
