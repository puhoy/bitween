from threading import Lock

import logging

logger = logging.getLogger(__name__)

from libtorrent import make_magnet_uri


class OwnShares:
    """
    holds a reference to the handles and some values for other threads

    this is managed by the bt thread
    """

    def __init__(self, handles):

        self.list = []
        self.lock = Lock()
        self.handles = handles
        self.rebuild(self.handles)

    def rebuild(self, torrentinfo_list):
        #logger.debug(self.list)
        self.list = []
        for info in torrentinfo_list:
            self.add(info)

    def add(self, info_dict):
        logger.debug('added file %s', info_dict['name'])
        with self.lock:
            #logger.info('new files: %s' % h)
            self.list.append(info_dict)

    def get(self, handle):
        with self.lock:
            for h in self.list:
                if h['handle'] is handle:
                    return h

    def remove(self, handle):
        logger.debug('removing handle')
        with self.lock:
            for h in self.list:
                if h['handle'] is '%s' % handle:
                    del h
                    return
                else:
                    logger.debug('%s is not %s' % (h['handle'], '%s' % handle))
            logger.debug('handle not found!')

    def __getitem__(self, key):
        return self.list[key]

    def __setitem__(self, key, value):
        self.list[key] = value

    def __delitem__(self, key):
        del self.list[key]

    def __iter__(self):
        with self.lock:
            for x in self.list:
                yield x
