from argh import ArghParser
from argh.decorators import aliases, arg
from getpass import getpass

from core import create_xmpp_client, main_xmpp_queue, xmpp_main_queue
from core import create_torrent_client, main_torrent_queue, torrent_main_queue

import logging

logging.basicConfig(level=logging.DEBUG)


@arg('jid', help='jabber id')
@arg('-p', '--password', help='password')
@arg('-s', nargs='*', type=str, help='list of files to share')
def start_xmpp(jid, password='', s=[]):
    if not password:
        password = getpass('password: ')

    create_xmpp_client(jid, password, main_xmpp_queue, xmpp_main_queue)


def start_torrent():
    create_torrent_client(main_torrent_queue, torrent_main_queue)


if __name__ == "__main__":
    parser = ArghParser()
    parser.add_commands([start_xmpp, start_torrent])
    parser.dispatch()
