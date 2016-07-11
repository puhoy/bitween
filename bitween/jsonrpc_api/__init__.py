"""
initialize the jsonrpc API

starts the api on /api, enables the web browsable api if "enable_web_api" is set to true in config
"""

import logging

logger = logging.getLogger(__name__)
logger.info('initializing %s' % __name__)
from models.config import conf
from models import contact_shares

from flask import Flask
from flask import request
from flask_jsonrpc import JSONRPC
from threading import Thread

enable_web_api = conf.get('enable_web_api', False)

app = Flask(__name__)
jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=enable_web_api)

from .bt import *
from .xmpp import *


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
    """
    return a list of all discovered bitween clients and their torrents

    :return:
    """
    return contact_shares.dict

class JsonRpcAPI(Thread):
    def __init__(self, api_host='localhost', api_port=8080):
        super(JsonRpcAPI, self).__init__()
        self.api_port = api_port
        self.api_host = api_host

    def run(self):
        app.run(host=self.api_host, port=self.api_port)
