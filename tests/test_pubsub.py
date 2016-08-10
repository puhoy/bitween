# -*- coding: utf-8 -*-

import unittest
import importlib
import imp

from bitween import components


class PubsubTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_publish_empty_subscribers(self):
        ret = components.publish('some_other_topic')
        assert ret is False

    def test_publish_with_subscribers(self):
        s = components.Subscriber()
        s.subscribe('some_topic')
        ret = components.publish('some_topic')
        assert ret is True

    def test_get_message(self):
        s = components.Subscriber()

        # subscribe a topic
        assert s.subscribe('some_topic') is True

        # try again
        assert s.subscribe('some_topic') is False

        # try get messages when empty
        assert s.has_messages() is False
        assert s.get_message() is False

        # publish & get
        assert components.publish('some_topic') is True
        assert s.has_messages() is True

        topic, args, kwargs = s.get_message()
        assert topic == 'some_topic'

    def test_publish_from_subscriber(self):
        s = components.Subscriber()
        s.subscribe('some_topic')

        s.publish('some_topic')
        assert s.has_messages() is True

    def test_autosubscribe(self):
        s = components.AutoSub()
        assert components.publish('some_topic') is True
        assert s.has_messages() is True


if __name__ == '__main__':
    unittest.main()
