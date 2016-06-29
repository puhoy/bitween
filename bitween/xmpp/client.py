import sys
import sleekxmpp
from ..pubsub import PubSubscriber
from . import share_plugin
from . import contact_shares
from . import own_shares
from . import own_addresses
from . import logger

class XmppClient(sleekxmpp.ClientXMPP, PubSubscriber):
    def __init__(self, jid, password):
        PubSubscriber.__init__(self, autosubscribe=True)
        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        self.add_event_handler("session_start", self.start)
        self.scheduler.add("_schedule", 2, self.process_queue, repeat=True)
        self.add_event_handler('shares_publish', self.on_shares_publish)

        self.register_plugin('xep_0004')
        self.register_plugin('xep_0030')
        self.register_plugin('xep_0060')
        self.register_plugin('xep_0115')
        self.register_plugin('xep_0118')
        self.register_plugin('xep_0128')
        self.register_plugin('xep_0163')
        self.register_plugin('shares', module=share_plugin)

        # self.auto_authorize = True
        # self.auto_subscribe = True

        self.name = 'xmpp_client_%s' % self.boundjid.bare

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

    def on_update_shares(self):
        logger.debug('publishing shares')
        self['shares'].publish_shares(own_shares, own_addresses)

    @staticmethod
    def on_shares_publish(msg):
        """ handle incoming files """
        incoming_shares = msg['pubsub_event']['items']['item']['shares']['share_items']
        addresses = msg['pubsub_event']['items']['item']['shares']['addresses']
        resource = msg['pubsub_event']['items']['item']['shares']['resource']

        logger.debug('got magnetlinks from %s' % msg['from'])
        contact = str(msg['from'])

        if incoming_shares is not None:
            contact_shares.clear_shares(contact, resource)
            # res = user_shares.get_resource(contact, resource)
            for d in incoming_shares:
                hash = d.attrib['hash']
                size = d.attrib['size']
                name = d.attrib['name']
                logger.debug('adding %s' % hash)
                contact_shares.add_share(jid=contact, resource=resource, hash=hash, name=name, size=size, files=[])
        else:
            logger.debug('No item content')

        if addresses is not None:
            contact_shares.clear_addresses(contact, resource)
            for d in addresses:
                contact_shares.add_address(jid=contact, resource=resource, address=d['address'], port=d['port'])

    def on_exit(self):
        logger.debug('sending empty shares')
        self['shares'].stop()
        self.disconnect(wait=True)
