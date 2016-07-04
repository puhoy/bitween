from bitween.log import setup_logging
import logging
import sys

from argparse import ArgumentParser



if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')
else:
    raw_input = input


def start(api_host, api_port):
    from bitween.sentinel import Sentinel
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
        setup_logging(default_level=logging.DEBUG)
    else:
        setup_logging(default_level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info('starting up')

    import time
    time.sleep(1)

    start(args.bind, args.port)
