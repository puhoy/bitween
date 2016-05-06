__author__ = 'meatpuppet'
# !/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

import sleekxmpp

from bitween.pubsub import PubSubscriber

from bitween.core.models import handlelist, user_shares

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
        PubSubscriber.__init__(self, autosubscribe=True)
        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        if not settings:
            settings = {}

        self.settings = settings

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
        self['xep_0115'].update_caps()

        #self['shares'].publish_shares(handlelist, handlelist.ip_address)

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
        h = [{'name': 'test',
              'hash': 'xxxxx',
              'size': 100}]
        ip_address = '1.1.1.1'
        self['shares'].publish_shares(h, ip_address)

    def on_update_shares(self):
        logger.debug('publishing shares')
        self['shares'].publish_shares(handlelist, handlelist.ip_address)

    @staticmethod
    def on_shares_publish(msg):
        """ handle incoming files """
        data = msg['pubsub_event']['items']['item']['payload']
        logger.debug('got magnetlinks from %s' % msg['from'])
        contact = str(msg['from'])
        resource = data.attrib.get('resource', '')
        ip = data.attrib.get('ip', '')

        # todo: ipv6
        if data is not None:
            logger.debug('data: %s' % data)
            if ip:
                user_shares.clear_shares(contact, resource)
                res = user_shares.get_resource(contact, resource)
                res['ip_v4'] = ip
                for d in data:
                    hash = d.attrib['hash']
                    size = d.attrib['size']
                    name = d.attrib['name']
                    logger.debug('adding %s' % hash)
                    user_shares.add_share(jid=contact, resource=resource, hash=hash, name=name, size=size, files=[])
        else:
            logger.debug('No item content')

    def on_exit(self):
        logger.debug('sending empty shares')
        self['shares'].stop(handlelist.ip_address)
        self.disconnect(wait=True)
