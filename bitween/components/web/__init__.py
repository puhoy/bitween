"""
initialize the jsonrpc API

starts the api on /api, enables the web browsable api if "enable_web_api" is set to true in config
"""

import logging

logger = logging.getLogger(__name__)
logger.info('initializing %s' % __name__)

from bitween.components.models import config
from .. import publish

from flask import Flask
from flask.ext.bootstrap import Bootstrap

from flask_jsonrpc import JSONRPC
from threading import Thread

from .gui import gui as gui_blueprint

conf = config.conf

enable_web_api = conf.get('enable_web_api', False)

app = Flask(__name__)
jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=enable_web_api)

from .api import versions, safe_exit
from .api.bt import get_torrents, add_path, add_torrent_by_hash, del_torrent
from .api.xmpp import get_all_hashes, get_all_shares

bootstrap = Bootstrap()
bootstrap.init_app(app)

app.register_blueprint(gui_blueprint)


class Web(Thread):
    """
    web thread
    starts the gui and the jsonrpc api
    """
    def __init__(self, api_host='localhost', api_port=8080):
        """
        initiate a new web class with api and basic gui

        :param api_host:
        :param api_port:
        """
        super(Web, self).__init__()
        self.api_port = api_port
        self.api_host = api_host

    def run(self):
        """
        start the thread

        triggered by .start()

        :return:
        """
        app.run(host=self.api_host, port=self.api_port)
