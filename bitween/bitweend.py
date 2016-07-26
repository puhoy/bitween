from log import setup_logging
import logging

from argparse import ArgumentParser

from components.xmpp import XmppClient
from components import config

conf = config.conf


def start(api_host, api_port):
    c = XmppClient(conf['xmpp_account']['jid'], conf['xmpp_account']['password'], api_host, api_port)
    c.connect()
    c.process()


def main(args=None):
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


if __name__ == "__main__":
    main()
