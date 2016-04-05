import logging
from threading import Thread

from .bt.base_client import TorrentSession
from .xmpp.base_client import XmppClientBase

logger = logging.getLogger(__name__)

from core.pubsub import publish, Subscriber
from core.rest import RestAPI
from types import FunctionType


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

    def __init__(self):
        Thread.__init__(self)
        Subscriber.__init__(self)
        self.subscribe('sentinel')
        # all functions starting with on_
        # modified from http://stackoverflow.com/questions/1911281/how-do-i-get-list-of-methods-in-a-python-class
        listen_to = [x for x, y in Sentinel.__dict__.items() if
                     (type(y) == FunctionType and x.startswith('on_'))]  # ['bt_ready', 'add_file']
        for l in listen_to:
            self.subscribe(l.split('on_')[1])
        self.name = 'sentinel'

    def _add_xmpp_client(self, jid, password):
        logger.info('creating new xmpp client for %s' % jid)
        c = create_xmpp_client(jid=jid, password=password)
        self.xmpp_clients.append({'client': c})

    def add_bt_client(self):
        c = create_torrent_client()
        self.bt_client = {'client': c}

    def run(self):
        self.add_bt_client()
        RestAPI().start()
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
        publish('generate_torrent', file)

    def on_new_handle(self):
        """
        updates the list of handles and triggers all xmpp clients to send the new file list
        """
        publish('magnet_links_publish')  # call method on xmpp clients
        pass
