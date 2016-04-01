from queue import Queue, Empty
from threading import Lock

import logging

logger = logging.getLogger(__name__)

topics = {}
lock = Lock()


def publish(topic, *args, **kwargs):
    t = get_topic(topic)
    logger.debug('got subscribers in topic: %s' % t['subscribers'])
    with lock:
        for s in t['subscribers']:
            logger.debug('published message on topic %s: %s %s' % (topic, args, kwargs))
            s.put((topic, args, kwargs))


def get_topic(topic):
    t = topics.get(topic, None)
    if not t:
        topics[topic] = new_topic()
        logger.debug('new topic %s' % topic)
        t = topics[topic]
    return t


def new_topic():
    return {
        'subscribers': []
    }


class Subscriber:
    def __init__(self, name=''):
        self.queue = Queue()
        self.name = name

    def subscribe(self, topic):
        t = get_topic(topic)
        with lock:
            if self not in t['subscribers']:
                t['subscribers'].append(self)
                return True
            else:
                logger.debug('already subscribed to %s' % topic)
                return False

    def put(self, topic, *args, **kwargs):
        self.queue.put(topic, *args, **kwargs)

    def has_messages(self):
        return self.queue.qsize() != 0

    def get(self):
        logger.debug('%s has messages' % self, )
        if self.has_messages():
            (topic, args, kwargs) = self.queue.get(block=False)
            return topic, args, kwargs
        return False

    def __del__(self):
        with lock:
            for t in topics:
                if self in t['subscribers']:
                    t['subscribers'].remove(self)
                    logger.debug('removed self from %s while deleting' % t)

    def __repr__(self):
        return self.name
