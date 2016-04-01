from queue import Queue, Empty
from threading import Lock

import logging

logger = logging.getLogger(__name__)

topics = {}
lock = Lock()


def publish(topic, *args, **kwargs):
    t = get_topic(topic)
    with lock:
        for s in t['subscribers']:
            s.put(topic, args, kwargs)


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
    def __init__(self):
        self.queue = Queue()

    def subscribe(self, topic):
        t = get_topic(topic)
        with lock:
            if self not in t['subscribers']:
                t['subscribers'].append(self)
                return True
            else:
                logger.debug('already subscribed to %s' % topic)
                return False

    def put(self, *args, **kwargs):
        self.queue.put(args, kwargs)

    def get(self):
        try:
            topic, args, kwargs = self.queue.get(block=False)
        except Empty:
            return None
        except:
            return False
        return topic, args, kwargs

    def __del__(self):
        with lock:
            for t in topics:
                if self in t['subscribers']:
                    t['subscribers'].remove(self)
                    logger.debug('removed self from %s while deleting' % t)
