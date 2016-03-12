from core.xmpp.base_client import XmppClientBase
from argh import ArghParser
from argh.decorators import aliases, arg
from getpass import getpass

import logging

logging.basicConfig(level=logging.DEBUG)

@arg('jid', help='jabber id')
@arg('-p', '--password', help='password')
@arg('-s', nargs='*', type=str, help='list of files to share')
def start_xmpp(jid, password='', s=[]):
    if not password:
        password = getpass('password: ')

    #logging.debug('shared: %s' % s)

    c = XmppClientBase(jid, password, shares=s)

    if c.connect():
        # If you do not have the dnspython library installed, you will need
        # to manually specify the name of the server if it does not match
        # the one in the JID. For example, to use Google Talk you would
        # need to use:
        #
        # if xmpp.connect(('talk.google.com', 5222)):
        #     ...
        c.process(blocking=False)
        #print("Done")
    else:
        logging.error("Unable to connect.")

    #c.connect()

if __name__ == "__main__":
    parser = ArghParser()
    parser.add_commands([start_xmpp])
    parser.dispatch()
