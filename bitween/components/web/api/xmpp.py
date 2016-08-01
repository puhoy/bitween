"""
XMPP related functions of the JSONRPCAPI
"""

from bitween.components.web import logger
from .. import jsonrpc
from bitween.components import contact_shares
from flask import jsonify


@jsonrpc.method('xmpp.add_account', jid='', password='')
def add_account(jid, password):
    """
    todo

    adds a new xmpp account

    :param jid:
    :param password:
    :return:
    """
    return jsonify({'todo': 'not implemented'})  # todo


@jsonrpc.method('xmpp.get_accounts')
def get_accounts():
    """
    todo

    :return: a list of current xmpp accounts
    """
    return jsonify({'todo': 'not implemented'})  # todo


@jsonrpc.method('xmpp.get_hashes')
def get_all_hashes():
    """
    return a list of all hashes with associated address tuples

    :return:
    """
    return jsonify({'hashes': contact_shares.hashes})

@jsonrpc.method('xmpp.get_shares')
def get_all_shares():
    """
    return a list of all collected shares

    :return:
    """
    return jsonify({'shares': contact_shares.dict})
