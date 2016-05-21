import os

import json
from flask import jsonify

from bitween.pubsub import publish
from . import jsonrpc
from bitween.core.models import own_shares
import logging
logger = logging.getLogger(__name__)
from .. import conf

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

"""
@jsonrpc.method('bt.get_magnet', torrentname='')
def get_mlink(torrentname=''):
    # magnet:?xt=urn:btih: Base16 encoded info-hash [ &dn= name of download ] [ &tr= tracker URL ]*
    mlink = None
    for h in own_shares:
        if h['name'] == torrentname:
            mlink = h['mlink']
            return mlink
    # not found
    return False
"""




"""
@jsonrpc.method('bt.add_peer', hash='', peer_address='', peer_port='')
def add_peer(hash, peer_address, peer_port):
    logger.debug('adding peer')
    for h in own_shares:
        if h['hash'] == hash:
            # found torrent, give it to bt module
            publish('add_peer', h['hash'], str(peer_address), int(peer_port))
            return True
"""

