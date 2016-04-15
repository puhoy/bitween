from threading import Thread

from flask import Flask, request
from flask_jsonrpc import JSONRPC

import logging

logger = logging.getLogger(__name__)

app = Flask(__name__)
jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)

# @jsonrpc.method('App.index', user='')
# def index(user='tester'):
#    return u'Welcome to Flask JSON-RPC, ' + user

from .bt import *
from .xmpp import *

from ..models import contactlist


@jsonrpc.method('Api.versions')
def versions():
    import libtorrent
    import sleekxmpp
    versions = {"libtorrent": '' + libtorrent.version,
                "sleekxmpp": '' + sleekxmpp.__version__}
    logger.debug(versions)
    return versions


@jsonrpc.method('Api.exit')
def safe_exit():
    publish('exit')
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@jsonrpc.method('Api.get_all_torrents')
def get_all_torrents():
    d = {}
    for k, v in contactlist.dict.iteritems():
        logger.debug('contact %s' % k)
        d[str(k)] = v.torrents_as_dict
    return d



class JsonRpcAPI(Thread):
    def __init__(self):
        super(JsonRpcAPI, self).__init__()

    def run(self):
        app.run(host='0.0.0.0')
