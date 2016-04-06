import os

from flask import jsonify

from bitween.pubsub import publish
from . import jsonrpc
from .. import handlelist


@jsonrpc.method('bt.get_torrents')
def get_torrents():
    torrents = []
    for t in handlelist:
        torrents.append(t)
    return jsonify(torrents)


@jsonrpc.method('bt.add_torrent', file=str)
def add_torrent(file=''):
    if os.path.isfile(file):
        publish('add_file', file)
        return True
    else:
        return False


@jsonrpc.method('bt.get_magnet', torrentname='')
def get_mlink(torrentname=''):
    # magnet:?xt=urn:btih: Base16 encoded info-hash [ &dn= name of download ] [ &tr= tracker URL ]*
    mlink = None
    for h in handlelist:
        if h['name'] == torrentname:
            mlink = h['mlink']
            return mlink
    # not found
    return False


@jsonrpc.method('bt.add_torrent_by_mlink', mlink='')
def add_torrent_by_mlink(mlink):
    publish('add_magnetlink', mlink)


@jsonrpc.method('bt.add_peer', torrentname='', peer_address='')
def add_peer(torrentname, peer_address):
    for h in handlelist:
        if h['name'] == torrentname:
            # found torrent, give it to bt module
            publish('add_peer', h['handle'], peer_address)
            return True
