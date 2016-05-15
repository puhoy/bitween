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

    def add(self, info):
        logger.debug('added file %s', info.name())
        with self.lock:
            #info = handle.get_torrent_info()
            h = {}

            #h['handle'] = '%s' % handle
            h['files'] = []

            try:
                h['total_size'] = info.total_size()
            except:
                h['total_size'] = 0
            try:
                h['name'] = info.name()
            except:
                h['name'] = ''
            try:
                h['hash'] = '%s' % info.info_hash()
            except:
                h['hash'] = ''

            try:
                files = info.files()  # the filestore object
            except:
                files = []

            for f in files:
                h['files'].append(
                    {
                        'path': f.path,  # filename for file at index f
                        # 'size': files.file_size(f)
                    })
            logger.info('new files: %s' % h)
            self.list.append(h)

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
