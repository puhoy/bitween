from threading import Thread

from flask import Flask, request
from flask_jsonrpc import JSONRPC

app = Flask(__name__)
jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)

# @jsonrpc.method('App.index', user='')
# def index(user='tester'):
#    return u'Welcome to Flask JSON-RPC, ' + user

from .bt import *
from .xmpp import *


@jsonrpc.method('main.exit')
def safe_exit():
    publish('exit')
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


class JsonRpcAPI(Thread):
    def __init__(self):
        super(JsonRpcAPI, self).__init__()

    def run(self):
        app.run(host='0.0.0.0')
