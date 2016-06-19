
from threading import Lock
import sys
import logging
from types import FunctionType

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
        logger.error('published to topic %s with no subscribers' % topic)
        return False
    with lock:
        for s in t['subscribers']:
            logger.debug('published message on topic %s: %s %s' % (topic, args, kwargs))
            s.put_message((topic, args, kwargs))
        return True


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


class PubSubscriber:
    def __init__(self, name='', autosubscribe=False):
        """

        :param name:
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
        t = _get_topic(topic)
        with lock:
            if self not in t['subscribers']:
                logger.debug('%s subscribed to %s' % (self.name, topic))
                t['subscribers'].append(self)
                return True
            else:
                logger.debug('already subscribed to %s' % topic)
                return False

    def put_message(self, topic, *args, **kwargs):
        self.queue.put(topic, *args, **kwargs)

    def has_messages(self, timeout=None):
        return self.queue.qsize() != 0

    def get_message(self, timeout=0.1):
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
        ret = publish(topic, *args, **kwargs)
        if not ret:
            logger.error('error at %s' % self)

    def __del__(self):
        with lock:
            if topics:
                for t in topics:
                    if self in t['subscribers']:
                        t['subscribers'].remove(self)
                        logger.debug('removed self from %s while deleting' % t)

    def __repr__(self):
        return self.name
