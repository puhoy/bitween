import logging
from threading import Thread

from .bt.base_client import TorrentSession
from .xmpp.base_client import XmppClientBase

logger = logging.getLogger(__name__)

from bitween.pubsub import publish, Subscriber
from bitween.core.api import JsonRpcAPI
from types import FunctionType


def create_xmpp_client(jid, password):
    c = XmppClientBase(jid, password)
    c.connect()
    c.process(threaded=True)
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
        self.name = 'sentinel'
        self.subscribe('sentinel')
        # all functions starting with on_
        # modified from http://stackoverflow.com/questions/1911281/how-do-i-get-list-of-methods-in-a-python-class
        listen_to = [x for x, y in Sentinel.__dict__.items() if
                     (type(y) == FunctionType and x.startswith('on_'))]  # ['bt_ready', 'add_file']
        for l in listen_to:
            self.subscribe(l.split('on_')[1])

        self.api = JsonRpcAPI()

        self.end = False

    def _add_xmpp_client(self, jid, password):
        logger.info('creating new xmpp client for %s' % jid)
        c = create_xmpp_client(jid=jid, password=password)
        self.xmpp_clients.append({'client': c})

    def add_bt_client(self):
        c = create_torrent_client()
        self.bt_client = {'client': c}

    def run(self):
        self.add_bt_client()
        self.api.start()
        logger.debug('starting loop')
        while not self.end:
            # news?
            ret = self.get()
            if ret:
                (topic, args, kwargs) = ret
                try:
                    f = getattr(self, 'on_%s' % topic)
                    logger.debug('calling %s' % f)
                    f(*args, **kwargs)
                except Exception as e:
                    logger.error('something went wrong when calling on_%s: %s' % (topic, e))

        logging.info('quitting')

    def on_bt_ready(self):
        """

        :return:
        """
        for xmpp_account in conf.get('xmpp_accounts', []):
            self._add_xmpp_client(xmpp_account['jid'], xmpp_account['password'])
        publish('update_magnetlinks')

    def on_add_file(self, file):
        logger.debug('adding file')
        publish('generate_torrent', file)

    def on_new_handle(self):
        """
        updates the list of handles and triggers all xmpp clients to send the new file list
        """
        publish('update_magnetlinks')  # call method on xmpp clients
        pass

    def on_exit(self):

        self.bt_client['client'].join()

        self.api.join()

        #for c in self.xmpp_clients:
        #    c['client'].join()

        self.end = True
