"""
Democlass for autosubscribing

needed for testing
"""


from .pubsub import Subscriber

class AutoSub(Subscriber):
    def __init__(self):
        Subscriber.__init__(self, autosubscribe=True)

    def process_messages(self):
        if self.has_messages():
            topic, args, kwargs = self.get_message()
        try:
            f = getattr(self, 'on_%s' % topic)
            f(*args, **kwargs)

        except Exception as e:
            print('something went wrong when calling on_%s: %s' % (topic, e))

    def on_some_topic(self, some_string, some_int=1):
        print('some_string is %s' % some_string)
        print('some_int is %s' % some_int)