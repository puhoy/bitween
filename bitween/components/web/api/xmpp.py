"""
XMPP related functions of the JSONRPCAPI
"""

from .. import jsonrpc
from bitween.components import contact_shares
from flask import jsonify


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
