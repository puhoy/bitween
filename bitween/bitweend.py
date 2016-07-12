from bitween.log import setup_logging
import logging
import sys


from argparse import ArgumentParser
import json
import os

import bitween
XmppClient = bitween.XmppClient
config = bitween.config


if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')
else:
    raw_input = input


def start(api_host, api_port):
    c = XmppClient(config['xmpp_account']['jid'], config['xmpp_account']['password'], api_host, api_port)
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
