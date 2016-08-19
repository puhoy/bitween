
from .. import jsonrpc
from .. import publish
from .. import logger

from flask import request



@jsonrpc.method('Api.versions')
def versions():
    """
    get the currently used versions of libtorrent and sleekxmpp

    :return:
    """
    import libtorrent
    import sleekxmpp
    versions = {"libtorrent": '' + libtorrent.version,
                "sleekxmpp": '' + sleekxmpp.__version__}
    logger.debug(versions)
    return versions

@jsonrpc.method('Api.exit')
def safe_exit():
    """
    trigger shutdown

    :return:
    """
    publish('exit')
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


