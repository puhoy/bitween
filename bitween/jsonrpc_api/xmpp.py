"""
XMPP related functions of the JSONRPCAPI
"""

from . import logger
from . import jsonrpc
from ..models import contact_shares
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
    return jsonify({'hashes': user_shares.hashes})
