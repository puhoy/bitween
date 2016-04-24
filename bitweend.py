from bitween.log import setup_logging
import logging

from argparse import ArgumentParser

from bitween.core.sentinel import Sentinel


setup_logging()
logger = logging.getLogger(__name__)


#@arg('jid', help='jabber id')
#@arg('-p', '--password', help='password')
#@arg('-s', nargs='*', type=str, help='list of files to share')
def start(api_host, api_port):
    s = Sentinel(api_host, api_port)
    s.start()
    s.join()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-p", "--port", default=5000)
    parser.add_argument("-b", "--bind", default='localhost')
    parser.add_argument("--debug", default=False, action='store_true')


    args = parser.parse_args()


    if args.debug:
        setup_logging(default_level=logging.INFO)
    else:
        setup_logging(default_level=logging.DEBUG)

    start(args.bind, args.port)