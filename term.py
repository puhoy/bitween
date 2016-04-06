import logging

from argh import ArghParser

from bitween.core.main import Sentinel

logger = logging.getLogger(__name__)


#@arg('jid', help='jabber id')
#@arg('-p', '--password', help='password')
#@arg('-s', nargs='*', type=str, help='list of files to share')
def start():
    s = Sentinel()
    s.start()
    s.join()


if __name__ == "__main__":
    parser = ArghParser()
    parser.add_commands([start])
    parser.dispatch()
