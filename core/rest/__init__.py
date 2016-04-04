from flask import Flask, jsonify
from flask_jsonrpc import JSONRPC

from threading import Thread

from .. import handlelist
from pubsub import publish

import os

app = Flask(__name__)
jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)


#@jsonrpc.method('App.index', user='')
#def index(user='tester'):
#    return u'Welcome to Flask JSON-RPC, ' + user

@jsonrpc.method('bt.torrents')
def get_torrents():
    torrents = []
    for t in handlelist:
        torrents.append(t)
    return jsonify(torrents)
    #return u'Welcome to Flask JSON-RPC, ' + user

@jsonrpc.method('bt.add_torrent', file='')
def add_torrent(file=''):
    if os.path.isfile(file):
        publish('add_file', file)
        return True
    else:
        return False





class RestAPI(Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        app.run(host='0.0.0.0')
