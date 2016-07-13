from . import logger

from threading import Lock
import sys
from types import FunctionType

if sys.version_info < (3, 0):
    import Queue as queue
    from Queue import Empty
else:
    import queue
    from queue import Empty

topics = {}

def publish(topic, *args, **kwargs):
    """
    publish arguments to a topic.

    :param topic: topic to publish the message to
    :type topic: str
    :param args: unnamed arguments
    :param kwargs: named arguments
    :return: False if no Subscribers, else True
    """
    t = _get_topic(topic)
    logger.debug('got subscribers in topic: %s' % t['subscribers'])
    if not t['subscribers']:
        logger.error('published to topic %s with no subscribers' % topic)
        return False
    with Lock():
        for s in t['subscribers']:
            logger.debug('published message on topic %s: %s %s' % (topic, args, kwargs))
            s._put_message((topic, args, kwargs))
        return True


def _get_topic(topic):
    """
    get a topic from the topics dictionary
    will be created new, with no subscribers, if there is none.

    :param topic:
    :return:
    """
    t = topics.get(topic, None)
    if not t:
        topics[topic] = _new_topic()
        logger.debug('new topic %s' % (topic))
        t = topics[topic]
    return t


def _new_topic():
    """
    create an empty dictionary with subscribers. used by _get_topic()

    :return: empty subscribers dict
    """
    return {
        'subscribers': []
    }


class Subscriber:
    def __init__(self, name='', autosubscribe=False):
        """
        Base Class for IPC

         all Subclasses inherit Queues and basic scheduling functions

         see the __init__.py of this module for example usage.

        :param name: Optional, but used in debugging
        :param autosubscribe: if True, subscribe to all functionnames starting with on_, without on_ ("on_topic()" would subscribe to "topic")
        :return:
        """
        self.queue = queue.Queue()
        self.name = name
        if autosubscribe:
            listen_to = [x for x, y in self.__class__.__dict__.items() if
                         (type(y) == FunctionType and x.startswith('on_'))]
            for l in listen_to:
                self.subscribe(l.split('on_')[1])

    def subscribe(self, topic):
        """
        manually subscribe a topic

        :param topic:
        :return:
        """
        t = _get_topic(topic)
        with Lock():
            if self not in t['subscribers']:
                logger.info('%s subscribed to %s' % (self.name, topic))
                t['subscribers'].append(self)
                return True
            else:
                logger.error('already subscribed to %s' % topic)
                return False

    def _put_message(self, topic, *args, **kwargs):
        """
        put a Message in the Queue.
        called by the publish-function

        :param topic:
        :param args:
        :param kwargs:
        :return:
        """
        self.queue.put(topic, *args, **kwargs)

    def has_messages(self):
        """

        :return: True if Queue not Empty, otherwise False
        """
        return self.queue.qsize() != 0

    def get_message(self, timeout=0.1):
        """
        get topic, arguments and names arguments

        :param timeout:
        :return: topic, args, kwargs
        :rtype: str, list, dict
        """
        try:
            (topic, args, kwargs) = self.queue.get(block=True, timeout=timeout)
            return topic, args, kwargs
        except Empty:
            return False

    def publish(self, topic, *args, **kwargs):
        """
        just for nicer logging output. calls the regular publish via this method

        :param topic:
        :param args:
        :param kwargs:
        :return:
        """
        logger.info('%s is publishing on topic %s: %s, %s' % (self.name, topic, args, kwargs))
        ret = publish(topic, *args, **kwargs)
        if not ret:
            logger.error('error at %s' % self)

    def __del__(self):
        with Lock():
            if topics:
                for t in topics:
                    if self in t['subscribers']:
                        t['subscribers'].remove(self)
                        logger.debug('removed self from %s while deleting' % t)

    def __repr__(self):
        return self.name
