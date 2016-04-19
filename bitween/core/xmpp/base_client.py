__author__ = 'meatpuppet'
# !/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

import sleekxmpp
from sleekxmpp.xmlstream import tostring

#import asyncio
from types import FunctionType

from bitween.pubsub import PubSubscriber

from .magnetlinkstanza import MagnetLinksStanza
from bitween.core.models import handlelist, contactlist

import logging

logger = logging.getLogger(__name__)


if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')
else:
    raw_input = input


class XmppClientBase(sleekxmpp.ClientXMPP, PubSubscriber):
    def __init__(self, jid, password, settings={}):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        PubSubscriber.__init__(self, autosubscribe=True)

        if not settings:
            settings = {}

        self.settings = settings
        self.register_plugin('xep_0030')  # Service Discovery
        self.register_plugin('xep_0199')  # XMPP Ping
        self.register_plugin('xep_0163')  # pep
        self.register_plugin('xep_0060')  # PubSub

        self.add_event_handler("session_start", self.start)


        self.name = 'xmpp_client_%s' % self.boundjid.bare
        # all functions starting with on_
        # modified from http://stackoverflow.com/questions/1911281/how-do-i-get-list-of-methods-in-a-python-class


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
        logger.debug('sending presence & getting roster')
        self.send_presence(ppriority=-128, pstatus='', ptype='xa')
        self.get_roster()
        # from https://groups.google.com/forum/#!topic/sleekxmpp-discussion/KVs5lMzVP70
        self['xep_0163'].add_interest('https://xmpp.kwoh.de/protocol/magnet_links')  # pep
        self['xep_0030'].add_feature('https://xmpp.kwoh.de/protocol/magnet_links')  # service discovery
        self['xep_0060'].map_node_event('https://xmpp.kwoh.de/protocol/magnet_links', 'magnet_links')  # pubsub
        self.add_event_handler('magnet_links_publish', self.on_magnet_links_publish)
        #self.add_event_handler('magnet_links_publish', self.on_magnet_links_publish)

        ## Generic pubsub event handlers for all nodes
        #
        # self.add_event_handler('pubsub_publish', handler)
        # self.add_event_handler('pubsub_retract', handler)
        # self.add_event_handler('pubsub_purge', handler)
        # self.add_event_handler('pubsub_delete', handler)



        self.scheduler.add("schedule", 2, self.process_queue, repeat=True)

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

    def on_update_magnetlinks(self):
        self['xep_0163'].publish(MagnetLinksStanza(handlelist), ifrom=self.boundjid.full)

    @staticmethod
    def on_magnet_links_publish(msg):
        """ handle incoming files """
        logging.debug('magnetlinks: %s' % msg)
        #logging.debug('Published item %s to %s:' % (
        #    msg['pubsub_event']['items']['item']['id'],
        #    msg['pubsub_event']['items']['node']))
        data = msg['pubsub_event']['items']['item']['payload']
        logger.debug('magnetlinks: %s' % msg)

        contact = contactlist.get_contact(str(msg['from']))
        if data is not None:
            contact.ip_v4 = data.attrib['ip']
            contacts_torrents = []
            for d in data:
                hash = d.text
                size = d.attrib['size']
                name = d.attrib['name']
                contacts_torrents.append({"hash": hash, "size": size, "name": name})
                logger.debug('got %s' % size)
            contact.set_torrents(contacts_torrents)
        else:
            logger.debug('No item content')


    def on_exit(self):
        self.disconnect(wait=True)


"""
# events

DEBUG:sleekxmpp.xmlstream.xmlstream:Event triggered: roster_update
DEBUG:root:got roster: {}
DEBUG:sleekxmpp.xmlstream.xmlstream:Event triggered: presence
DEBUG:sleekxmpp.xmlstream.xmlstream:Event triggered: presence_available
DEBUG:sleekxmpp.xmlstream.xmlstream:Event triggered: got_online
DEBUG:sleekxmpp.xmlstream.xmlstream:Event triggered: changed_status
DEBUG:sleekxmpp.xmlstream.xmlstream:Event triggered: sent_presence


## presence subscription

DEBUG:sleekxmpp.xmlstream.xmlstream:RECV: <presence to="bitween@xmpp.kwoh.de" from="jan@xmpp.kwoh.de" type="subscribe" />
DEBUG:sleekxmpp.xmlstream.xmlstream:Event triggered: presence
DEBUG:sleekxmpp.xmlstream.xmlstream:Event triggered: presence_subscribe
DEBUG:sleekxmpp.xmlstream.xmlstream:Event triggered: changed_subscription
DEBUG:sleekxmpp.xmlstream.xmlstream:Event triggered: roster_subscription_request
DEBUG:sleekxmpp.xmlstream.xmlstream:SEND: <presence xml:lang="en" to="jan@xmpp.kwoh.de" type="subscribed" />
DEBUG:sleekxmpp.xmlstream.xmlstream:SEND: <presence xml:lang="en" to="jan@xmpp.kwoh.de" />
DEBUG:sleekxmpp.xmlstream.xmlstream:SEND: <presence xml:lang="en" to="jan@xmpp.kwoh.de" type="subscribe" />
DEBUG:sleekxmpp.xmlstream.xmlstream:RECV: <iq type="set" id="lx23"><query xmlns="jabber:iq:roster" ver="2"><item jid="jan@xmpp.kwoh.de" subscription="from" /></query></iq>
DEBUG:sleekxmpp.xmlstream.xmlstream:Event triggered: roster_update
DEBUG:sleekxmpp.xmlstream.xmlstream:SEND: <iq id="lx23" type="result"><query xmlns="jabber:iq:roster" /></iq>
DEBUG:sleekxmpp.xmlstream.xmlstream:RECV: <iq type="set" id="lx25"><query xmlns="jabber:iq:roster" ver="3"><item jid="jan@xmpp.kwoh.de" subscription="from" ask="subscribe" /></query></iq>
DEBUG:sleekxmpp.xmlstream.xmlstream:RECV: <presence to="bitween@xmpp.kwoh.de" from="jan@xmpp.kwoh.de" type="unavailable" />
DEBUG:sleekxmpp.xmlstream.xmlstream:Event triggered: roster_update
DEBUG:sleekxmpp.xmlstream.xmlstream:Event triggered: presence
DEBUG:sleekxmpp.xmlstream.xmlstream:Event triggered: presence_unavailable
DEBUG:sleekxmpp.xmlstream.xmlstream:SEND: <iq id="lx25" type="result"><query xmlns="jabber:iq:roster" /></iq>

"""
