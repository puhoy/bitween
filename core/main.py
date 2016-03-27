import asyncio
from .xmpp.base_client import XmppClientBase
from .bt.base_client import TorrentSession

from queue import Queue, Empty
from threading import Thread, Lock
import logging

logger = logging.getLogger(__name__)


def create_xmpp_client(jid, password, input_queue, output_queue):
    c = XmppClientBase(jid, password, input_queue=input_queue, output_queue=output_queue)
    c.connect()
    c.process()
    return c


def create_torrent_client(main_bt_queue, bt_main_queue):
    ts = TorrentSession(main_bt_queue, bt_main_queue)
    ts.start()
    return ts

from . import conf, handlelist


class Sentinel(Thread):
    """
    should keep track of clients and torrens
    """
    xmpp_clients = []
    bt_client = {}

    files = handlelist

    def __init__(self):
        super().__init__()
        self.in_queue = Queue()

    def _add_xmpp_client(self, jid: str, password: str) -> dict:
        logger.info('creating new xmpp client for %s' % jid)

        in_queue = Queue()
        out_queue = Queue()

        c = create_xmpp_client(jid=jid, password=password, input_queue=in_queue, output_queue=out_queue)
        self.xmpp_clients.append({'client': c,
                                  'in_queue': in_queue,
                                  'out_queue': out_queue})

    def add_bt_client(self):

        in_queue = Queue()
        out_queue = Queue()

        c = create_torrent_client(in_queue, out_queue)

        self.bt_client = {'client': c,
                          'in_queue': in_queue,
                          'out_queue': out_queue}

    def run(self):
        self.add_bt_client()
        logger.debug('starting loop')
        while True:
            # news?
            for client in self.xmpp_clients + [self.bt_client]:
                try:
                    items = client['out_queue'].get(block=False)
                    f_name = items[0]
                    args = items[1:]
                    logger.debug('calling %s(%s)' % (f_name, args))
                    f = getattr(self, 'on_%s' % f_name)
                    f(*args)
                except Empty:
                    pass
            try:
                items = self.in_queue.get(block=False)
                f_name = items[0]
                args = items[1:]
                logger.debug('calling %s(%s)' % (f_name, args))
                f = getattr(self, 'on_%s' % f_name)
                f(*args)
            except Empty:
                pass


    def on_bt_ready(self):
        for xmpp_account in conf.get('xmpp_accounts', []):
            self._add_xmpp_client(xmpp_account['jid'], xmpp_account['password'])
        #self.in_queue.put(['add_file', 'shared/df'])

    def on_add_file(self, file):
        logger.debug('adding file')
        self.bt_client['in_queue'].put(['generate_torrent', file])


