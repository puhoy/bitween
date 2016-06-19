from . import jsonrpc
from bitween.pubsub import publish
from flask import jsonify
from ..models import user_shares

@jsonrpc.method('xmpp.add_account', jid='', password='')
def add_account(jid, password):
    return jsonify({'todo': 'not implemented'})  # todo


@jsonrpc.method('xmpp.get_accounts')
def add_account(jid, password):
    return jsonify({'todo': 'not implemented'})  # todo


@jsonrpc.method('xmpp.get_hashes')
def get_all_hashes():
    """
    return a list of all hashes with associated address tuples

    :return:
    """
    return jsonify({'hashes': user_shares.hashes})
