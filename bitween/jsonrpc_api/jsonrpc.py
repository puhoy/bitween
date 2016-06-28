"""
initialize the jsonrpc API

starts the api on /api, enables the web browsable api if "enable_web_api" is set to true in config
"""
from .. import conf

from flask import Flask
from flask_jsonrpc import JSONRPC

enable_web_api = conf.get('enable_web_api', False)

app = Flask(__name__)
jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=enable_web_api)

from .bt import *
from .xmpp import *
#from .debug import *
