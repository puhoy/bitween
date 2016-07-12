from log import setup_logging
import logging
import sys


from argparse import ArgumentParser
import json
import os

from components.xmpp import XmppClient
from components import config

conf = config.conf


if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')
else:
    raw_input = input


def start(api_host, api_port):
    c = XmppClient(conf['xmpp_account']['jid'], conf['xmpp_account']['password'], api_host, api_port)
    c.connect()
    c.process()

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-p", "--port", default=5000)
    parser.add_argument("-b", "--bind", default='localhost')
    parser.add_argument("--debug", default=False, action='store_true')

    args = parser.parse_args()

    if args.debug:
        setup_logging(default_level=logging.DEBUG)
    else:
        setup_logging(default_level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info('starting up')

    start(args.bind, args.port)
