__author__ = 'meatpuppet'
# !/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

import sleekxmpp
import logging
import xml.etree.cElementTree as et
from sleekxmpp.xmlstream import tostring
import asyncio
import json

import logging
import log

logger = logging.getLogger(__name__)

from queue import Empty

if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')
else:
    raw_input = input


class MagnetLinksStanza(object):
    def __init__(self, magnetlinks):
        root = et.Element("magnet_links")
        for l in magnetlinks:
            link = et.Element("link")
            link.text = l
            root.append(link)
        self.xml = root
        self.namespace = 'https://xmpp.kwoh.de/protocol/magnet_links'


class XmppClientBase(sleekxmpp.ClientXMPP):
    def __init__(self, jid, password, settings={}, input_queue=None, output_queue=None, shares=[]):
        super(XmppClientBase, self).__init__(jid, password)

        if not settings:
            settings = {}

        self.input_queue = input_queue
        self.output_queue = output_queue
        self.shares = shares

        self.settings = settings
        self.register_plugin('xep_0030')  # Service Discovery
        self.register_plugin('xep_0199')  # XMPP Ping
        self.register_plugin('xep_0163')  # pep
        self.register_plugin('xep_0060')  # PubSub

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
        logger.debug('sending presence & getting roster')
        self.send_presence(ppriority=-128, pstatus='', ptype='xa')
        self.get_roster()
        # from https://groups.google.com/forum/#!topic/sleekxmpp-discussion/KVs5lMzVP70
        self['xep_0163'].add_interest('https://xmpp.kwoh.de/protocol/magnet_links')  # pep
        self['xep_0030'].add_feature('https://xmpp.kwoh.de/protocol/magnet_links')  # service discovery
        self['xep_0060'].map_node_event('https://xmpp.kwoh.de/protocol/magnet_links', 'magnet_links')  # pubsub
        self.add_event_handler('magnet_links_publish', self.on_magnet_links_publish)

        ## Generic pubsub event handlers for all nodes
        #
        # self.add_event_handler('pubsub_publish', handler)
        # self.add_event_handler('pubsub_retract', handler)
        # self.add_event_handler('pubsub_purge', handler)
        # self.add_event_handler('pubsub_delete', handler)

        self['xep_0163'].publish(MagnetLinksStanza(self.shares))

        self.scheduler.add("asyncio_queue", 2, self.process_queue,
            repeat=True, qpointer=self.event_queue)

    def process_queue(self):
        '''
        do something with the queue here

        :return:
        '''
        try:
            msg = self.input_queue.get(False) #doesn't block
            #logger.info("got msg from main: %s" % msg)
            # schedule the reply
            #scheduler.Task("SEND REPLY", 0, self.send_reply, (msg,)).run()
        except Empty:
            pass
        pass

    @staticmethod
    def on_magnet_links_publish(msg):
        """ handle incoming files """
        print('Published item %s to %s:' % (
            msg['pubsub_event']['items']['item']['id'],
            msg['pubsub_event']['items']['node']))
        data = msg['pubsub_event']['items']['item']['payload']
        if data is not None:
            for d in data:
                print(d.text)
                print(tostring(d))
        else:
            print('No item content')

    ##
    #  async commands
    ##
    @asyncio.coroutine
    def add_mlinks(self, mlinks):
        """

        :param mlinks: a list of magnet links
        :return:
        """
        pass

    @asyncio.coroutine
    def del_mlinks(self, mlinks):
        pass


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
