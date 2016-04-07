
from threading import Lock
import sys
import logging

if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')
    import Queue as queue
    from Queue import Empty
else:
    raw_input = input
    import queue
    from queue import Empty


logger = logging.getLogger(__name__)

topics = {}
lock = Lock()


"""
## how to pubsub

### create a subscriber and subscribe min. one topic
e.g.

s = Subscriber()
s.subscribe('myTopic')

### then post to the topic:

publish('myTopic', 'somestring', val=123)


### get that message by defining some loop

def loop():
    while True:
        if self.has_messages():
            (topic, args, kwargs) = self.get()
            print('%s, %s, %s' % topic, args, kwargs)



## the whole thing as a class

class MySub(Subscriber):
    def __init__(self):
        super().__init__()
        self.subscribe('myTopic')
        self.loop()

    def loop():
        while True:
            if self.has_messages():
                (topic, args, kwargs) = self.get()
                print('%s, %s, %s' % topic, args, kwargs)

"""


def publish(topic, *args, **kwargs):
    """
    publish to a topic.
    """

    t = _get_topic(topic)
    logger.debug('got subscribers in topic: %s' % t['subscribers'])
    if not t['subscribers']:
        logger.error('published to topic with no subscribers')
        return False
    with lock:
        for s in t['subscribers']:
            logger.debug('published message on topic %s: %s %s' % (topic, args, kwargs))
            s.put((topic, args, kwargs))


def _get_topic(topic):
    t = topics.get(topic, None)
    if not t:
        topics[topic] = _new_topic()
        logger.debug('new topic %s' % (topic))
        t = topics[topic]
    return t


def _new_topic():
    return {
        'subscribers': []
    }


class Subscriber:
    def __init__(self, name=''):
        self.queue = queue.Queue()
        self.name = name

    def subscribe(self, topic):
        t = _get_topic(topic)
        with lock:
            if self not in t['subscribers']:
                logger.debug('%s subscribed to %s' % (self.name, topic))
                t['subscribers'].append(self)
                return True
            else:
                logger.debug('already subscribed to %s' % topic)
                return False

    def put(self, topic, *args, **kwargs):
        self.queue.put(topic, *args, **kwargs)

    def has_messages(self, timeout=None):
        return self.queue.qsize() != 0

    def get(self, timeout=0.1):
        try:
            (topic, args, kwargs) = self.queue.get(block=True, timeout=timeout)
            return topic, args, kwargs
        except Empty:
            return False

    def __del__(self):
        with lock:
            if topics:
                for t in topics:
                    if self in t['subscribers']:
                        t['subscribers'].remove(self)
                        logger.debug('removed self from %s while deleting' % t)

    def __repr__(self):
        return self.name
