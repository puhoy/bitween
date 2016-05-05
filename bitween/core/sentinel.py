import logging
from threading import Thread

from .bt.base_client import TorrentClient
from .xmpp.base_client import XmppClient


logger = logging.getLogger(__name__)

from bitween.pubsub import PubSubscriber
from bitween.core.api import JsonRpcAPI
import ipgetter

def create_xmpp_client(jid, password):
    c = XmppClient(jid, password)
    c.connect()
    c.process()
    return c


def create_torrent_client():
    ts = TorrentClient()
    ts.start()
    return ts


from . import conf
from bitween.core.models import handlelist


class Sentinel(Thread, PubSubscriber):
    """
    should keep track of clients and torrens
    """
    xmpp_clients = []
    bt_client = {}

    files = handlelist

    def __init__(self, api_host, api_port=8080):
        Thread.__init__(self)
        PubSubscriber.__init__(self, autosubscribe=True)
        self.name = 'sentinel'
        # all functions starting with on_
        # modified from http://stackoverflow.com/questions/1911281/how-do-i-get-list-of-methods-in-a-python-class


        self.api = JsonRpcAPI(api_host, api_port)

        self.end = False

        self.ip_v4 = ''
        self.ip_v6 = ''
        self.got_ip = False

    def get_ip_address(self, ipv4='', ipv6=''):
        """
        listen for ip from libtorrent

        :param ipv4:
        :param ipv6:
        :return:
        """
        logger.debug('getting own external ip...')
        # todo: this is ipv4 only
        self.ip_v4 = ipv4
        self.ip_v6 = ipv6

        self.ip_v4 = ipgetter.myip()

        if self.ip_v6 or self.ip_v4:
            self.got_ip = True
            logger.debug('got ip: %s' % self.ip_v4)
            handlelist.ip_address = self.ip_v4
            self.add_bt_client()

    def _add_xmpp_client(self, jid, password):
        logger.info('creating new xmpp client for %s' % jid)
        c = create_xmpp_client(jid=jid, password=password)
        self.xmpp_clients.append({'client': c})

    def add_bt_client(self):
        c = create_torrent_client()
        self.bt_client = {'client': c}

    def run(self):
        #self.add_bt_client()
        self.get_ip_address()
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

        logging.info('quitting')

    def on_bt_ready(self):
        """

        :return:
        """
        for xmpp_account in conf.get('xmpp_accounts', []):
            self._add_xmpp_client(xmpp_account['jid'], xmpp_account['password'])
        #self.publish('update_magnetlinks')

    def on_add_file(self, file):
        logger.debug('adding file')
        self.publish('generate_torrent', file)

    def on_new_handle(self):
        """
        updates the list of handles and triggers all xmpp clients to send the new file list
        """
        self.publish('update_magnetlinks')  # call method on xmpp clients
        pass

    def on_exit(self):

        self.bt_client['client'].join()

        self.api.join()

        # for c in self.xmpp_clients:
        #    c['client'].join()
        # todo: this breaks sleekxmpp while quitting, but i think it should join (?)

        self.end = True
