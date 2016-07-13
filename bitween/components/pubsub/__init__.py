"""
PubSub for interprocess communication

holds topics to subscribe and methods to publish to those topics.

usage
=====

basic::

    # create the subscriber object ans subscribe to topic 'myTopic'

    s = Subscriber()
    s.subscribe('myTopic')

    def loop():
        while True:
            if s.has_messages():
                (topic, args, kwargs) = s.get()
                print('%s, %s, %s' % topic, args, kwargs)

    # (maybe from another thread and object) post to the topic:

    publish('myTopic', 'somestring', val=123)


by subclassing::

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
import logging
logger = logging.getLogger(__name__)
logger.info('starting %s' % __name__)

from .pubsub import publish, Subscriber
from autosubscriber import AutoSub