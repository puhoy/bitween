import sys
import sleekxmpp
from .. import Subscriber

from .. import contact_shares
from .. import handles
from .. import Addresses

from . import logger
from . import share_plugin

from .. import BitTorrentClient
from .. import Web

from .. import publish

def create_torrent_client():
    ts = BitTorrentClient()
    ts.start()
    return ts


class XmppClient(Subscriber, sleekxmpp.ClientXMPP):
    def __init__(self, jid, password, api_host='localhost', api_port=8080):
        Subscriber.__init__(self, autosubscribe=True)
        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        self.add_event_handler("session_start", self.start)

        self.register_plugin('xep_0030')  # service discovery
        self.register_plugin('xep_0115')  # entity caps
        self.register_plugin('xep_0128')  # service discovery extensions
        self.register_plugin('xep_0163')  # pep

        self.register_plugin('shares', module=share_plugin)
        self.add_event_handler('shares_publish', self.on_shares_publish)

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
        Process the session_start event.

        Typical actions for the session_start event are
        requesting the roster and broadcasting an initial
        presence stanza.

        Arguments:
            event -- An empty dictionary. The session_start
                     event does not provide any additional
                     data.

        """
        logger.debug('sending presence & getting roster for %s' % self.boundjid)

        self.send_presence()
        self.get_roster()

        self.publish('publish_shares')

    def process_queue(self):
        '''
        do something with the queue here

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
        logger.debug('publishing shares')
        self['shares'].publish_shares(handles.get_shares(), self.addresses)

    @staticmethod
    def on_shares_publish(msg):
        """ handle incoming files """
        incoming_shares = msg['pubsub_event']['items']['item']['user_shares']
        logger.info('%s' % incoming_shares)

        contact_shares.clear(msg['from'])

        for resource in incoming_shares['resources']:
            logger.info('processing the following res: %s' % resource)
            logger.info('clearing resource %s of user %s' % (resource['resource'], msg['from']))
            contact_shares.clear(msg['from'], resource['resource'])

            for item in resource['share_items']:
                logger.info('adding share %s to resource %s' % (item['name'], resource['resource']))
                contact_shares.add_share(msg['from'], resource['resource'], item['hash'], item['name'], item['size'])

            for address in resource['ip_addresses']:
                contact_shares.add_address(msg['from'], resource['resource'], address['address'], address['port'])

        publish('recheck_handles')

    def on_set_port(self, port):
        # todo
        pass

    def on_exit(self):
        logger.debug('sending empty shares')
        self['shares'].stop()

        self.bt_client.join()
        self.api.join()

        self.disconnect(wait=True)
