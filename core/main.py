from .xmpp.base_client import XmppClientBase
from .bt.base_client import TorrentSession

from threading import Thread
import logging

logger = logging.getLogger(__name__)

from pubsub import publish, Subscriber


def create_xmpp_client(jid, password):
    c = XmppClientBase(jid, password)
    c.connect()
    c.process()
    return c


def create_torrent_client():
    ts = TorrentSession()
    ts.start()
    return ts


from . import conf, handlelist


class Sentinel(Thread, Subscriber):
    """
    should keep track of clients and torrens
    """
    xmpp_clients = []
    bt_client = {}

    files = handlelist

    listen_to = ['bt_ready', 'add_file']



    def __init__(self):
        Thread.__init__(self)
        Subscriber.__init__(self)
        self.subscribe('sentinel')
        for l in self.listen_to:
            self.subscribe(l)
        self.name = 'sentinel'

    def _add_xmpp_client(self, jid: str, password: str) -> dict:
        logger.info('creating new xmpp client for %s' % jid)
        c = create_xmpp_client(jid=jid, password=password)
        self.xmpp_clients.append({'client': c})

    def add_bt_client(self):
        c = create_torrent_client()
        self.bt_client = {'client': c}

    def run(self):
        self.add_bt_client()
        logger.debug('starting loop')
        while True:
            # news?
            if self.has_messages():
                (topic, args, kwargs) = self.get()
                try:
                    f = getattr(self, 'on_%s' % topic)
                    f(*args, **kwargs)
                except:
                    logger.error('something went wrong when calling on_%s' % topic)

    def on_bt_ready(self):
        """

        """
        for xmpp_account in conf.get('xmpp_accounts', []):
            self._add_xmpp_client(xmpp_account['jid'], xmpp_account['password'])
            # self.in_queue.put(['add_file', 'shared/df'])

    def on_add_file(self, file):
        logger.debug('adding file')
        self.bt_client['in_queue'].put(['generate_torrent', file])
