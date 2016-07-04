from threading import Thread
from bitween.pubsub import PubSubscriber

from . import logger
from .. import conf


from .. import models


models.contact_shares = models.ContactShares()
models.own_shares = models.OwnShares([])

from ..bt import BitTorrentClient
from ..xmpp import XmppClient
from ..jsonrpc_api import JsonRpcAPI


def create_xmpp_client(jid, password):
    c = XmppClient(jid, password)
    c.connect()
    c.process()
    return c


def create_torrent_client():
    ts = BitTorrentClient()
    ts.start()
    return ts


class Sentinel(Thread, PubSubscriber):
    """
    should keep track of clients and torrens
    """
    xmpp_clients = []
    bt_client = {}

    def __init__(self, api_host, api_port=8080):
        Thread.__init__(self)
        PubSubscriber.__init__(self, autosubscribe=True)
        self.name = 'sentinel'
        # all functions starting with on_
        # modified from http://stackoverflow.com/questions/1911281/how-do-i-get-list-of-methods-in-a-python-class

        self.api = JsonRpcAPI(api_host, api_port)
        self.end = False
        self.got_ip = False
        self.bt_ready = False

        models.own_addresses = models.Addresses()

    def _add_xmpp_client(self, jid, password):
        logger.info('creating new xmpp client for %s' % jid)
        c = create_xmpp_client(jid=jid, password=password)
        self.xmpp_clients.append({'client': c})

    def add_bt_client(self):
        c = create_torrent_client()
        self.bt_client = {'client': c}

    def run(self):
        self.api.start()
        logger.debug('starting loop')
        while not self.end:
            # news?
            ret = self.get_message()
            if ret:
                (topic, args, kwargs) = ret
                try:
                    f = getattr(self, 'on_%s' % topic)
                    logger.debug('calling %s' % f)
                    f(*args, **kwargs)
                except Exception as e:
                    logger.error('something went wrong when calling on_%s: %s' % (topic, e))

        logger.info('quitting')

    def on_bt_ready(self):
        models.own_addresses.ports.append(self.bt_client['client'].session.listen_port())
        # self.own_addresses.port = self.bt_client['client'].session.ssl_listen_port()
        for xmpp_account in conf.get('xmpp_accounts', []):
            self._add_xmpp_client(xmpp_account['jid'], xmpp_account['password'])
        self.bt_ready = True
        self.publish('publish_shares')

    def on_got_ip(self):
        self.got_ip = True
        self.add_bt_client()

    def on_set_port(self, port):
        logger.debug('setting external port to %s' % port)
        own_addresses.nat_ports = [port]
        logger.debug('new nat port list: %s' % own_addresses.nat_ports)
        self.publish('publish_shares')

    def on_add_file(self, file):
        logger.debug('adding file')
        self.publish('generate_torrent', file)

    def on_publish_shares(self):
        """
        updates the list of handles and triggers all xmpp clients to send the new file list
        """
        if self.got_ip and self.bt_ready:
            self.publish('update_shares')  # call method on xmpp clients
        else:
            print('%s %s' % (self.got_ip, self.bt_ready))

    def on_exit(self):

        self.bt_client['client'].join()

        self.api.join()

        # for c in self.xmpp_clients:
        #    c['client'].join()

        self.end = True
