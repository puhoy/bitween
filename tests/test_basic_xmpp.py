import unittest
import importlib
import imp
from bitween.xmpp import XmppClient
from bitween.pubsub import publish
from time import sleep


class BasicXMPPTestSuite(unittest.TestCase):
    """Basic XMPP test cases."""

    def test_xmpp_connects_and_exits(self):
        c1 = XmppClient("u1@localhost", 12345)
        c1.connect()

        publish('exit')
        c1.process()

        # print(c1.state)
        assert c1.state.current_state() == 'connected'

        publish('exit')
        sleep(3)
        assert c1.state.current_state() == 'disconnected'


if __name__ == '__main__':
    unittest.main()