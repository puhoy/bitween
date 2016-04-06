from . import jsonrpc
from bitween.pubsub import publish
from flask import jsonify

@jsonrpc.method('xmpp.add_account', jid='', password='')
def add_account(jid, password):
    return jsonify({'todo': 'not implemented'})  # todo
    #return u'Welcome to Flask JSON-RPC, ' + user


@jsonrpc.method('xmpp.get_accounts')
def add_account(jid, password):
    return jsonify({'todo': 'not implemented'})  # todo