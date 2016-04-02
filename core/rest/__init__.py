from flask import Flask
from flask_jsonrpc import JSONRPC

from threading import Thread

app = Flask(__name__)
jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)


@jsonrpc.method('App.index', user='')
def index(user='tester'):
    return u'Welcome to Flask JSON-RPC, ' + user


class RestAPI(Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        app.run(host='0.0.0.0')
