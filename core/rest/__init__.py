from threading import Thread

from flask import Flask
from flask_jsonrpc import JSONRPC

app = Flask(__name__)
jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)

#@jsonrpc.method('App.index', user='')
#def index(user='tester'):
#    return u'Welcome to Flask JSON-RPC, ' + user

from .bt import *
from .xmpp import *


class RestAPI(Thread):
    def __init__(self):
        super(RestAPI, self).__init__()

    def run(self):
        app.run(host='0.0.0.0')
