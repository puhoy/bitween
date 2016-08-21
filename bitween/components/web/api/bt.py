"""
BitTorrent related functions of the JSONRPCAPI
"""

from .. import logger

import os

from flask import jsonify

from bitween.components.pubsub import publish
from .. import jsonrpc
from bitween.components import handles


@jsonrpc.method('bt.get_torrents')
def get_torrents():
    """
    return a list of own torrents

    :return:
    """
    torrents = []
    for t in handles.get_shares():
        torrents.append(t)
    return jsonify({"torrents": torrents})


@jsonrpc.method('bt.add_path', path='')
def add_path(path=''):
    """
    create a torrent by path

    :param path: Path of folder or file to share
    :return:
    """
    logger.info('adding %s to torrents' % os.path.abspath(path))
    if os.path.exists(path):
        publish('generate_torrent', os.path.abspath(path))
        return True
    else:
        logger.error('error: %s does not exist' % os.path.abspath(path))
        return False


@jsonrpc.method('bt.add_torrent_by_hash', hash='', save_path=None)
def add_torrent_by_hash(hash, save_path):
    """
    add a new torrent based on hash

    :param hash: hash of the torrent
    :param save_path: path to save the torrent
    :return:
    """
    logger.info('adding hash %s to torrents' % hash)
    publish('add_hash', hash, save_path)


@jsonrpc.method('bt.del_torrent', hash='')
def del_torrent(hash):
    """
    delete a torrent by hash

    :param hash:
    :return:
    """
    logger.info('deleting torrent %s' % hash)
    publish('del_torrent', hash)
