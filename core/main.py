import asyncio
from .xmpp.base_client import XmppClientBase
from .bt.base_client import TorrentSession

from queue import Queue, Empty
from threading import Thread
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


class Sentinel(Thread):
    """
    should keep track of clients and torrens
    """
    xmpp_clients = []
    bt_client = {}

    files = []

    def __init__(self):
        super().__init__()
        self.add_bt_client()

    def add_xmpp_client(self, jid, password):
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
        logger.debug('starting loop')
        while True:
            # news?
            for client in self.xmpp_clients + [self.bt_client]:
                try:
                    (f, args, kwargs) = client['out_queue'].get(block=False)
                    logger.debug('calling %s(%s, %s)' % (f, args, kwargs))
                    f(args, kwargs)
                except Empty:
                    pass



