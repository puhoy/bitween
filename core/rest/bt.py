from flask import jsonify

from core.pubsub import publish
from . import jsonrpc
from .. import handlelist


@jsonrpc.method('bt.get_torrents')
def get_torrents():
    torrents = []
    for t in handlelist:
        torrents.append(t)
    return jsonify(torrents)
    #return u'Welcome to Flask JSON-RPC, ' + user

@jsonrpc.method('bt.add_torrent', file=str)
def add_torrent(file=''):
    #if os.path.isfile(file):
    publish('add_file', file)
#        return True
#    else:
#        return False