__author__ = 'meatpuppet'
# !/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

import sleekxmpp


from bitween.pubsub import PubSubscriber



from bitween.core.models import handlelist, contactlist

import logging
import random
from . import share_plugin

logger = logging.getLogger(__name__)


if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')
else:
    raw_input = input


class XmppClient(sleekxmpp.ClientXMPP, PubSubscriber):
    def __init__(self, jid, password, settings={}):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        PubSubscriber.__init__(self, autosubscribe=True)

        if not settings:
            settings = {}

        self.settings = settings
        self.add_event_handler('magnet_links_publish', self.on_magnet_links_publish)
        #self.register_plugin('xep_0030')  # Service Discovery
        self.register_plugin('xep_0199')  # XMPP Ping
        #self.register_plugin('xep_0060')  # PubSub
        #self.register_plugin('xep_0115')  # Entity Caps
        #self.register_plugin('xep_0163')  # pep

        self.register_plugin('xep_0004')
        self.register_plugin('xep_0030')
        self.register_plugin('xep_0060')
        self.register_plugin('xep_0115')
        self.register_plugin('xep_0118')
        #self.register_plugin('xep_0128')
        self.register_plugin('xep_0163')
        self.register_plugin('shares', module=share_plugin)


        self.name = 'xmpp_client_%s' % self.boundjid.bare
        # all functions starting with on_
        # modified from http://stackoverflow.com/questions/1911281/how-do-i-get-list-of-methods-in-a-python-class

        self.add_event_handler("session_start", self.start)

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

        self.send_presence(ppriority=1)
        self.get_roster()

        # from https://groups.google.com/forum/#!topic/sleekxmpp-discussion/KVs5lMzVP70

        logger.debug('sending presence & getting roster')

        self.on_update_magnetlinks()


        ## Generic pubsub event handlers for all nodes
        #
        self.add_event_handler('shares_publish', self.on_magnet_links_publish)
        # self.add_event_handler('pubsub_retract', handler)
        # self.add_event_handler('pubsub_purge', handler)
        # self.add_event_handler('pubsub_delete', handler)

        self.scheduler.add("_schedule", 2, self.process_queue, repeat=True)

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


    def on_send_handles(self):
        """
        for debugging purposes only

        :return:
        """
        from ..models import HandleList
        h = [{'name': 'test',
             'hash': 'xxxxx',
             'size': 100}]
        ip_address = '1.1.1.1'
        self['shares'].publish_shares(h, ip_address)

    def on_del_handles(self):
        """
        for debugging purposes only

        :return:
        """
        self['xep_0060'].purge(self.boundjid, self.create_magnetlink_stanza().namespace)
        self['xep_0060'].delete_node(self.boundjid, self.create_magnetlink_stanza().namespace)

    def on_update_magnetlinks(self):
        logging.debug('publishing magnetlinks')
        #self['xep_0163'].publish(self.create_magnetlink_stanza())
        self['shares'].publish_shares(handlelist, handlelist.ip_address)

    #@staticmethod
    def on_magnet_links_publish(self, msg):
        """ handle incoming files """
        data = msg['pubsub_event']['items']['item']['payload']
        logger.debug('got magnetlinks from %s' % msg['from'].full)
        logger.debug('!!! MESSAGE: %s' % msg)

        contact = contactlist.get_contact(str(msg['from'].full))
        if data is not None:
            logger.debug('data: %s' % data)
            contact.ip_v4 = data.attrib.get('ip', False)
            if contact.ip_v4:
                contacts_torrents = []
                for d in data:
                    hash = d.text
                    size = d.attrib['size']
                    name = d.attrib['name']
                    contacts_torrents.append({"hash": hash, "size": size, "name": name})
                #logger.debug('setting new torrents: %s' % contacts_torrents)
                contact.set_torrents(contacts_torrents)
        else:
            logger.debug('No item content')

    def on_exit(self):
        logger.debug('sending empty shares')
        self['shares'].stop()
        self.disconnect(wait=True)



