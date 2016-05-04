from . import jsonrpc
from bitween.pubsub import publish
from flask import jsonify


@jsonrpc.method('debug.send_empty_handles')
def send_empty_handles():
    """
    debugging: send empty handles and dummy ip
    :return:
    """
    publish('send_handles')

@jsonrpc.method('debug.send_delete_node')
def send_empty_handles():
    """
    debugging: send empty handles and dummy ip
    :return:
    """
    publish('del_handles')
