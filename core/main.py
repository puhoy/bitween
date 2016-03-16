import asyncio, slixmpp
from .xmpp.base_client import XmppClientBase


def create_xmpp_client(jid, password, main_xmpp_queue, xmpp_main_queue):
    c = XmppClientBase(jid, password, input_queue=main_xmpp_queue, output_queue=xmpp_main_queue)
    c.connect()
    c.process()
    return c


def create_bt_client():
    pass
