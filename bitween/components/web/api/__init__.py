
from .. import jsonrpc
from .. import publish

from flask import request
from components import contact_shares



@jsonrpc.method('Api.versions')
def versions():
    import libtorrent
    import sleekxmpp
    versions = {"libtorrent": '' + libtorrent.version,
                "sleekxmpp": '' + sleekxmpp.__version__}
    logger.debug(versions)
    return versions


@jsonrpc.method('Api.exit')
def safe_exit():
    publish('exit')
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@jsonrpc.method('Api.get_all_torrents')
def get_all_torrents():
    """
    return a list of all discovered bitween clients and their torrents

    :return:
    """
    return contact_shares.dict

