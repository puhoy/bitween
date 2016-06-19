from . import jsonrpc
from bitween.pubsub import publish


@jsonrpc.method('debug.send_empty_handles')
def send_empty_handles():
    """
    debugging: send empty handles and dummy ip
    :return:
    """
    publish('send_handles')

@jsonrpc.method('debug.resend_handles')
def resend_handles():
    """
    debugging: send empty handles and dummy ip
    :return:
    """
    publish('update_shares')

