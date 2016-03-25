import asyncio
from .xmpp.base_client import XmppClientBase
from .bt.base_client import TorrentSession

def create_xmpp_client(jid, password, main_xmpp_queue, xmpp_main_queue):
    c = XmppClientBase(jid, password, input_queue=main_xmpp_queue, output_queue=xmpp_main_queue)
    c.connect()
    c.process()



def create_torrent_client(main_bt_queue, bt_main_queue):
    ts = TorrentSession(main_bt_queue, bt_main_queue)
    ts.start()

