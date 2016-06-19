import os

from flask import jsonify

from bitween.pubsub import publish
from . import jsonrpc
from bitween.core.models import own_shares

import logging
logger = logging.getLogger(__name__)

@jsonrpc.method('bt.get_torrents')
def get_torrents():
    torrents = []
    for t in own_shares:
        torrents.append(t)
    return jsonify({"torrents": torrents})


@jsonrpc.method('bt.add_file', file='')
def add_file(file=''):
    if os.path.exists(file):
        publish('add_file', file)
        return True
    else:
        return False


@jsonrpc.method('bt.add_torrent_by_hash', mlink='', save_path=None)
def add_torrent_by_hash(hash, save_path):
    logging.debug('adding hash %s to torrents' % hash)
    publish('add_hash', hash, save_path)
