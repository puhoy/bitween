"""
BitTorrent related functions of the JSONRPCAPI
"""

from . import logger

import os

from flask import jsonify

from pubsub import publish
from . import jsonrpc
from models import own_shares


@jsonrpc.method('bt.get_torrents')
def get_torrents():
    torrents = []
    for t in own_shares:
        torrents.append(t)
    return jsonify({"torrents": torrents})


@jsonrpc.method('bt.add_file', file='')
def add_file(file=''):
    logger.info('adding %s to torrents' % file)
    if os.path.exists(file):
        publish('add_file', file)
        return True
    else:
        logger.error('error: %s does not exist' % file)
        return False


@jsonrpc.method('bt.add_torrent_by_hash', mlink='', save_path=None)
def add_torrent_by_hash(hash, save_path):
    logger.info('adding hash %s to torrents' % hash)
    publish('add_hash', hash, save_path)
