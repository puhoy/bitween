import sys
import sleekxmpp
from bitween.components.pubsub import Subscriber

from bitween.components.models import handles
from bitween.components.models import Addresses

from . import logger
from . import share_plugin

from bitween.components.bt import BitTorrentClient
from bitween.components.web import Web

def create_torrent_client():
    ts = BitTorrentClient()
    ts.start()
    return ts


class XmppClient(Subscriber, sleekxmpp.ClientXMPP):
    """
    XmppClient class

    """
    def __init__(self, jid, password, api_host='localhost', api_port=8080):
        """
        Initialize a new XmppClient Object: fetch Addresses, start the API on api_host:api_port and start the BT Client

        :param jid:
        :param password:
        :param api_host:
        :param api_port:
        """
        Subscriber.__init__(self, autosubscribe=True)
        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        self.add_event_handler("session_start", self.start)

        self.register_plugin('xep_0030')  # service discovery
        self.register_plugin('xep_0115')  # entity caps
        self.register_plugin('xep_0163')  # pep

        self.register_plugin('shares', module=share_plugin)

        self.scheduler.add("_schedule", 2, self.process_queue, repeat=True)

        # self.auto_authorize = True
        # self.auto_subscribe = True

        self.name = 'xmpp_client_%s' % self.boundjid.bare

        self.addresses = Addresses()
        self.addresses.fetch_addresses()

        logger.info('got addresses: %s' % (self.addresses.ip_v4 + self.addresses.ip_v6))

        self.api = Web(api_host, api_port)
        self.api.start()

        self.bt_client = BitTorrentClient()
        self.bt_client.start()

        self.addresses.ports.append(self.bt_client.session.listen_port())

    def start(self, event):
        """
        Process the start_event

        :param event: start event
        :return:
        """
        logger.debug('sending presence & getting roster for %s' % self.boundjid)

        self.send_presence()
        self.get_roster()

        self.publish('publish_shares')

    def process_queue(self):
        '''
        Processes the IPC Message Queue

        :return:
        '''
        if self.has_messages():
            topic, args, kwargs = self.get_message()
            try:
                f = getattr(self, 'on_%s' % topic)
                f(*args, **kwargs)
            except Exception as e:
                logger.error('something went wrong when calling on_%s: %s' % (topic, e))

    def on_publish_shares(self):
        """
        triggers the publishing of the own shares

        :return:
        """
        logger.debug('publishing shares')
        self['shares'].publish_shares(handles.get_shares(), self.addresses)

    def on_set_port(self, port):
        """
        set a NAT Port to send with the shares

        :param port: Port number
        :type port: int
        :return:
        """
        self.addresses.nat_ports.append(port)
        logger.info('found nat port %s' % port)

    def on_exit(self):
        """
        trigger shutdown

        :return:
        """
        logger.debug('sending empty shares')
        self['shares'].stop()

        self.bt_client.join()
        self.api.join()

        self.disconnect(wait=True)
